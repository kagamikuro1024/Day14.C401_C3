"""
BenchmarkRunner — Async pipeline đánh giá toàn bộ dataset.
Hỗ trợ retry khi rate limit, cost tracking và incremental saving.
"""
import asyncio
import os
import json
import re
import time
from typing import List, Dict
from engine.retrieval_eval import RetrievalEvaluator


class BenchmarkRunner:
    """Async runner để benchmark TA_Chatbot với đầy đủ metrics và cost tracking."""

    # Giá per 1M tokens (USD)
    PRICING = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-5.4-mini": {"input": 1.10, "output": 4.40},
        "gpt-5.4-nano": {"input": 0.15, "output": 0.60},
    }

    def __init__(self, agent, judge):
        self.agent = agent
        self.judge = judge
        self.retrieval_eval = RetrievalEvaluator()

    def _calculate_cost(self, usage: Dict, model: str) -> float:
        """Tính chi phí dựa trên token usage."""
        pricing = self.PRICING.get(model, {"input": 0, "output": 0})
        prompt_cost = (usage.get("prompt_tokens", 0) / 1_000_000) * pricing["input"]
        completion_cost = (usage.get("completion_tokens", 0) / 1_000_000) * pricing["output"]
        return round(prompt_cost + completion_cost, 6)

    async def run_single_test(self, test_case: Dict, max_retries: int = 5) -> Dict:
        """Chạy một case test với retry tự động khi gặp rate limit (429)."""
        for attempt in range(max_retries):
            try:
                start_time = time.perf_counter()

                # 1. Gọi Agent
                response = await self.agent.query(test_case["question"])
                latency = round(time.perf_counter() - start_time, 3)

                answer = response.get("answer", "")
                retrieved_ids = response.get("retrieved_ids", [])

                # 2. Tính Retrieval Metrics
                expected_ids = test_case.get("expected_retrieval_ids", [])
                retrieval_result = self.retrieval_eval.evaluate(
                    retrieved_ids=retrieved_ids,
                    expected_ids=expected_ids,
                )

                # 3. Multi-Judge Evaluation
                judge_result = await self.judge.evaluate_multi_judge(
                    question=test_case["question"],
                    answer=answer,
                    ground_truth=test_case.get("expected_answer", ""),
                )

                # 4. Tính cost
                total_usage = judge_result.get("total_usage", {})
                total_cost = 0.0
                for model, usage in total_usage.items():
                    total_cost += self._calculate_cost(usage, model)

                status = "pass" if judge_result["final_score"] >= 3.5 else "fail"

                return {
                    "test_case_id": test_case.get("question", "")[:50],
                    "question": test_case["question"],
                    "agent_response": answer,
                    "expected_answer": test_case.get("expected_answer", ""),
                    "difficulty": test_case.get("difficulty", "unknown"),
                    "type": test_case.get("type", "unknown"),
                    "latency": latency,
                    "retrieval": retrieval_result,
                    "judge": judge_result,
                    "cost_usd": round(total_cost, 6),
                    "status": status,
                }

            except Exception as e:
                err_str = str(e)
                if "429" in err_str and attempt < max_retries - 1:
                    # Parse thời gian chờ từ message API
                    wait_match = re.search(r'try again in (\d+(?:\.\d+)?)(ms|s)', err_str)
                    if wait_match:
                        val = float(wait_match.group(1))
                        unit = wait_match.group(2)
                        wait_sec = val / 1000 if unit == "ms" else val
                    else:
                        wait_sec = 10.0 * (attempt + 1)
                    wait_sec = min(wait_sec + 3, 65)  # Buffer 3s, tối đa 65s
                    print(f"  [429] Rate limit hit - waiting {wait_sec:.1f}s (attempt {attempt+1}/{max_retries})...", flush=True)
                    await asyncio.sleep(wait_sec)
                else:
                    return {
                        "question": test_case.get("question", "N/A"),
                        "error": err_str,
                        "status": "error",
                        "cost_usd": 0.0,
                    }

        return {
            "question": test_case.get("question", "N/A"),
            "error": "Max retries exceeded",
            "status": "error",
            "cost_usd": 0.0,
        }

    async def run_all(self, dataset: List[Dict], batch_size: int = 5) -> List[Dict]:
        """Chạy toàn bộ dataset theo batch với incremental saving."""
        results = []
        total = len(dataset)
        total_batches = (total + batch_size - 1) // batch_size

        print(f"[*] Bat dau Benchmark: {total} cases | Batch: {batch_size}", flush=True)
        os.makedirs("reports", exist_ok=True)

        for i in range(0, total, batch_size):
            batch = dataset[i:i + batch_size]
            batch_num = i // batch_size + 1
            print(f"  [{batch_num}/{total_batches}] Processing cases {i+1}-{min(i+batch_size, total)}...", flush=True)

            tasks = [self.run_single_test(case) for case in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            # Lưu kết quả tức thì sau mỗi batch
            with open("reports/benchmark_partial.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            passed = sum(1 for r in results if r.get("status") == "pass")
            errors = sum(1 for r in results if r.get("status") == "error")
            total_cost = sum(r.get("cost_usd", 0) for r in results)
            print(f"  [OK] {len(results)}/{total} done | Pass: {passed} | Error: {errors} | Cost: ${total_cost:.4f}", flush=True)

            # Delay giữa batch để tránh rate limit
            if i + batch_size < total:
                await asyncio.sleep(2)

        return results
