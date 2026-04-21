import asyncio
import time
from typing import List, Dict, Optional
from engine.retrieval_eval import RetrievalEvaluator

class BenchmarkRunner:
    """Async runner để benchmark TA_Chatbot với đầy đủ metrics và cost tracking."""

    def __init__(self, agent, judge):
        self.agent = agent
        self.judge = judge
        self.retrieval_eval = RetrievalEvaluator()
        
        # Giá per 1M tokens (USD) - Cập nhật 2024
        self.PRICING = {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gemini-1.5-pro": {"input": 3.50, "output": 10.00}
        }

    def _calculate_cost(self, usage: Dict, model: str) -> float:
        """Tính toán chi phí dựa trên usage và model pricing."""
        if model not in self.PRICING:
            return 0.0
        
        rates = self.PRICING[model]
        in_tokens = usage.get("prompt_tokens", 0)
        out_tokens = usage.get("completion_tokens", 0)
        
        cost = (in_tokens / 1_000_000 * rates["input"]) + (out_tokens / 1_000_000 * rates["output"])
        return round(cost, 6)

    async def run_single_test(self, test_case: Dict) -> Dict:
        """Chạy 1 test case qua toàn bộ pipeline: Agent -> Metrics -> Judge."""
        start_time = time.perf_counter()
        
        try:
            # 1. Gọi Agent (Inference)
            agent_result = await self.agent.query(test_case["question"])
            latency = time.perf_counter() - start_time
            
            answer = agent_result.get("answer", "")
            retrieved_ids = agent_result.get("retrieved_ids", [])
            
            # 2. Tính Retrieval Metrics (Hit Rate & MRR)
            expected_ids = test_case.get("expected_retrieval_ids", [])
            hit_rate = self.retrieval_eval.calculate_hit_rate(expected_ids, retrieved_ids)
            mrr = self.retrieval_eval.calculate_mrr(expected_ids, retrieved_ids)
            
            # 3. Chạy Multi-Judge (Evaluation)
            judge_result = await self.judge.evaluate_multi_judge(
                test_case["question"],
                answer,
                test_case.get("expected_answer", "")
            )
            
            # 4. Tính toán chi phí
            openai_usage = judge_result.get("total_usage", {}).get("openai", {})
            gemini_usage = judge_result.get("total_usage", {}).get("gemini", {})
            
            cost_openai = self._calculate_cost(openai_usage, "gpt-4o")
            cost_gemini = self._calculate_cost(gemini_usage, "gemini-1.5-pro")
            total_cost = round(cost_openai + cost_gemini, 6)

            return {
                "test_case_id": test_case.get("question", "")[:50],
                "question": test_case["question"],
                "agent_response": answer,
                "expected_answer": test_case.get("expected_answer", ""),
                "latency": round(latency, 2),
                "retrieval": {
                    "hit_rate": hit_rate,
                    "mrr": mrr,
                    "retrieved_ids": retrieved_ids[:3]
                },
                "judge": judge_result,
                "cost_usd": total_cost,
                "status": "pass" if judge_result["final_score"] >= 3.5 else "fail"
            }
            
        except Exception as e:
            return {
                "question": test_case["question"],
                "status": "error",
                "error": str(e)
            }

    async def run_all(self, dataset: List[Dict], batch_size: int = 5) -> List[Dict]:
        """
        Chạy toàn bộ dataset song song theo nhóm (Batch) để đảm bảo tốc độ và tránh Rate Limit.
        """
        results = []
        total = len(dataset)
        
        print(f"🚀 Bắt đầu Benchmark cho {total} cases (Batch Size: {batch_size})...")
        
        for i in range(0, total, batch_size):
            batch = dataset[i:i + batch_size]
            print(f"  [>] Processing cases {i+1} to {min(i + batch_size, total)}...")
            
            tasks = [self.run_single_test(case) for case in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            # Nghỉ ngắn giữa các batch để tránh spam API
            if i + batch_size < total:
                await asyncio.sleep(1)
        
        return results
