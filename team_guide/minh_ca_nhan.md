# 📋 Kế Hoạch Cá Nhân — Minh

> **Vai trò:** Contributor — Phát triển Async Benchmark Runner + Cost Tracking
> **Nhánh Git:** `feature/minh-async-runner`
> **Độ khó task:** ⭐⭐⭐ Trung bình - Khó

---

## 🎯 Nhiệm Vụ Của Minh

Minh chịu trách nhiệm **hoàn thiện Async Benchmark Runner** — hệ thống chạy toàn bộ pipeline đánh giá **song song và nhanh** (< 2 phút cho 50 cases). Đây là thành phần đảm bảo điểm **Performance/Async** trong rubric (10 điểm).

**Mục tiêu cụ thể:**
- Toàn bộ pipeline chạy async (không có blocking call)
- Batch processing với rate limit protection
- Báo cáo chi tiết về Cost & Token usage
- Regression Testing: so sánh V1 vs V2 với Release Gate tự động

---

## 📁 File Cần Sửa

- **Sửa:** `engine/runner.py` (hoàn thiện async pipeline)
- **Sửa:** `main.py` (hoàn thiện regression + release gate)

---

## 🌿 Bước 1: Tạo nhánh Git

```powershell
cd d:\gitHub\AI_20k\Day14\Lab14-AI-Evaluation-Benchmarking

git checkout main
git pull origin main

git checkout -b feature/minh-async-runner
git branch
# Xác nhận: * feature/minh-async-runner
```

---

## 💻 Bước 2: Implement `engine/runner.py`

Thay toàn bộ nội dung file:

```python
"""
BenchmarkRunner — Async pipeline chạy đánh giá toàn bộ dataset.

Đặc điểm:
- Chạy song song bằng asyncio.gather theo từng batch
- Giới hạn batch size để tránh API rate limit
- Tracking latency, cost, token usage chi tiết
- Xử lý lỗi riêng từng test case (không crash toàn bộ pipeline)
"""
import asyncio
import time
import traceback
from typing import List, Dict, Optional, Any

from engine.retrieval_eval import RetrievalEvaluator


# Ngưỡng Release Gate — thay đổi để điều chỉnh điều kiện approve
RELEASE_GATE_CONFIG = {
    "min_avg_score": 3.5,       # Điểm judge tối thiểu để APPROVE
    "min_hit_rate": 0.7,        # Hit rate tối thiểu
    "min_agreement_rate": 0.6,  # Agreement rate tối thiểu giữa 2 judges
    "max_fail_rate": 0.3,       # Tỷ lệ fail tối đa được chấp nhận
}


class CostTracker:
    """Theo dõi chi phí và token usage trong quá trình benchmark."""

    # Giá GPT-4o (USD per 1M tokens) — cập nhật theo OpenAI pricing
    GPT4O_INPUT_PRICE = 2.50    # $2.50 / 1M input tokens
    GPT4O_OUTPUT_PRICE = 10.00  # $10.00 / 1M output tokens
    
    # Gemini-2.5-Pro (ước tính)
    GEMINI_INPUT_PRICE = 1.25   # $1.25 / 1M input tokens
    GEMINI_OUTPUT_PRICE = 5.00  # $5.00 / 1M output tokens

    def __init__(self):
        """Khởi tạo tracker với các counter bằng 0."""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_api_calls = 0
        self.estimated_cost_usd = 0.0
        self.call_log = []      # Log chi tiết từng API call

    def record_call(
        self, 
        model: str, 
        input_tokens: int, 
        output_tokens: int
    ) -> None:
        """Ghi nhận 1 API call vào tracker."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_api_calls += 1
        
        # Ước tính chi phí
        if "gpt" in model.lower():
            cost = (input_tokens * self.GPT4O_INPUT_PRICE / 1_000_000 +
                    output_tokens * self.GPT4O_OUTPUT_PRICE / 1_000_000)
        elif "gemini" in model.lower():
            cost = (input_tokens * self.GEMINI_INPUT_PRICE / 1_000_000 +
                    output_tokens * self.GEMINI_OUTPUT_PRICE / 1_000_000)
        else:
            cost = 0.0
            
        self.estimated_cost_usd += cost
        self.call_log.append({
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost, 6),
        })

    def get_summary(self) -> Dict[str, Any]:
        """Trả về báo cáo tổng hợp chi phí."""
        return {
            "total_api_calls": self.total_api_calls,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "estimated_cost_usd": round(self.estimated_cost_usd, 4),
            "avg_cost_per_case_usd": round(
                self.estimated_cost_usd / max(self.total_api_calls // 2, 1), 4
            ),
        }


class BenchmarkRunner:
    """
    Async runner để benchmark TA_Chatbot trên toàn bộ golden dataset.
    
    Quy trình mỗi test case:
    1. Gọi Agent → lấy answer + retrieved_ids
    2. Tính Retrieval Metrics (Hit Rate + MRR)
    3. Chạy Multi-Judge (GPT-4o + Gemini song song)
    4. Tổng hợp kết quả + status pass/fail
    """

    def __init__(self, agent, evaluator, judge):
        """
        Khởi tạo runner với các components.
        
        Args:
            agent: MainAgent — interface async để gọi TA_Chatbot
            evaluator: (optional) RAGAS evaluator
            judge: LLMJudge — Multi-Judge engine
        """
        self.agent = agent
        self.evaluator = evaluator
        self.judge = judge
        self.retrieval_eval = RetrievalEvaluator()
        self.cost_tracker = CostTracker()

    async def run_single_test(self, test_case: Dict) -> Dict:
        """
        Chạy 1 test case qua toàn bộ pipeline.
        
        Xử lý lỗi riêng từng bước — nếu 1 bước lỗi thì vẫn tiếp tục.
        
        Args:
            test_case: Dict với question, expected_answer, expected_retrieval_ids
            
        Returns:
            Dict kết quả đầy đủ
        """
        start_time = time.perf_counter()
        question = test_case.get("question", "")

        # === BƯỚC 1: Gọi Agent ===
        try:
            agent_result = await self.agent.query(question)
            answer = agent_result.get("answer", "")
            retrieved_ids = agent_result.get("retrieved_ids", [])
        except Exception as e:
            answer = f"[AGENT ERROR: {str(e)[:100]}]"
            retrieved_ids = []

        latency = time.perf_counter() - start_time

        # === BƯỚC 2: Tính Retrieval Metrics ===
        expected_ids = test_case.get("expected_retrieval_ids", [])
        if expected_ids:
            hit_rate = self.retrieval_eval.calculate_hit_rate(expected_ids, retrieved_ids, top_k=3)
            mrr = self.retrieval_eval.calculate_mrr(expected_ids, retrieved_ids)
        else:
            # Nếu không có expected_ids, không tính metrics này
            hit_rate = None
            mrr = None

        # === BƯỚC 3: Chạy Multi-Judge ===
        try:
            judge_result = await self.judge.evaluate_multi_judge(
                question,
                answer,
                test_case.get("expected_answer", ""),
            )
            
            # Record cost (ước tính token usage)
            self.cost_tracker.record_call("gpt-4o", input_tokens=500, output_tokens=100)
            self.cost_tracker.record_call("gemini-2.5-pro", input_tokens=500, output_tokens=100)
            
        except Exception as e:
            judge_result = {
                "final_score": 0.0,
                "agreement_rate": 0.0,
                "conflict_detected": False,
                "individual_scores": {"gpt-4o": 0, "gemini-2.5-pro": 0},
                "error": str(e),
            }

        # === BƯỚC 4: Xác định status ===
        final_score = judge_result.get("final_score", 0)
        status = "pass" if final_score >= RELEASE_GATE_CONFIG["min_avg_score"] else "fail"

        return {
            "test_case_id": test_case.get("id", f"case_{hash(question) % 10000}"),
            "question": question,
            "agent_response": answer,
            "expected_answer": test_case.get("expected_answer", ""),
            "latency_seconds": round(latency, 3),
            "retrieval": {
                "hit_rate": hit_rate,
                "mrr": mrr,
                "retrieved_ids_preview": retrieved_ids[:3],
            },
            "judge": judge_result,
            "status": status,
            "metadata": {
                "difficulty": test_case.get("difficulty", "unknown"),
                "type": test_case.get("type", "unknown"),
            },
        }

    async def run_all(
        self, 
        dataset: List[Dict], 
        batch_size: int = 5,
        delay_between_batches: float = 1.5,
    ) -> List[Dict]:
        """
        Chạy toàn bộ dataset song song theo batch.
        
        Args:
            dataset: Danh sách test cases
            batch_size: Số cases chạy song song trong 1 batch (default 5)
            delay_between_batches: Độ trễ giữa batch (giây) — tránh rate limit
            
        Returns:
            Danh sách kết quả cho tất cả cases
        """
        results = []
        total = len(dataset)
        total_batches = (total + batch_size - 1) // batch_size
        
        start_total = time.perf_counter()
        print(f"  🔋 Tổng: {total} cases | Batch size: {batch_size} | Batches: {total_batches}")

        for i in range(0, total, batch_size):
            batch = dataset[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            print(f"  🔄 Batch {batch_num}/{total_batches} ({len(batch)} cases)...", end=" ")
            batch_start = time.perf_counter()
            
            # Chạy tất cả cases trong batch SONG SONG
            tasks = [self.run_single_test(case) for case in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            batch_elapsed = time.perf_counter() - batch_start
            print(f"✅ ({batch_elapsed:.1f}s)")
            
            # Xử lý kết quả, bao gồm exceptions
            for result in batch_results:
                if isinstance(result, Exception):
                    print(f"    ⚠️ Exception trong batch: {result}")
                    results.append({
                        "status": "error",
                        "error": str(result),
                        "judge": {"final_score": 0, "agreement_rate": 0},
                        "retrieval": {"hit_rate": None, "mrr": None},
                    })
                else:
                    results.append(result)
            
            # Delay giữa batches (ngoại trừ batch cuối)
            if i + batch_size < total:
                await asyncio.sleep(delay_between_batches)

        total_elapsed = time.perf_counter() - start_total
        print(f"  ⏱️  Tổng thời gian: {total_elapsed:.1f}s ({total_elapsed/60:.1f} phút)")
        print(f"  💰 Chi phí ước tính: ${self.cost_tracker.get_summary()['estimated_cost_usd']}")
        
        return results

    def check_release_gate(self, results: List[Dict]) -> Dict[str, Any]:
        """
        Kiểm tra Release Gate — quyết định có APPROVE hay BLOCK release.
        
        Logic:
        - Tính các metrics tổng hợp từ results
        - So sánh với ngưỡng trong RELEASE_GATE_CONFIG
        - Trả về decision + chi tiết
        """
        valid_results = [r for r in results if r.get("status") != "error"]
        total = len(valid_results)
        
        if total == 0:
            return {"approved": False, "reason": "Không có kết quả hợp lệ"}
        
        # Tính metrics
        avg_score = sum(r["judge"]["final_score"] for r in valid_results) / total
        
        results_with_hr = [r for r in valid_results if r["retrieval"]["hit_rate"] is not None]
        avg_hit_rate = (sum(r["retrieval"]["hit_rate"] for r in results_with_hr) / len(results_with_hr)
                       if results_with_hr else None)
        
        avg_agreement = sum(r["judge"].get("agreement_rate", 0) for r in valid_results) / total
        fail_count = sum(1 for r in valid_results if r["status"] == "fail")
        fail_rate = fail_count / total
        
        # So sánh với ngưỡng
        checks = {
            "avg_score_ok": avg_score >= RELEASE_GATE_CONFIG["min_avg_score"],
            "hit_rate_ok": avg_hit_rate is None or avg_hit_rate >= RELEASE_GATE_CONFIG["min_hit_rate"],
            "agreement_ok": avg_agreement >= RELEASE_GATE_CONFIG["min_agreement_rate"],
            "fail_rate_ok": fail_rate <= RELEASE_GATE_CONFIG["max_fail_rate"],
        }
        
        approved = all(checks.values())
        
        return {
            "approved": approved,
            "decision": "✅ APPROVE" if approved else "❌ BLOCK RELEASE",
            "metrics": {
                "avg_score": round(avg_score, 3),
                "avg_hit_rate": round(avg_hit_rate, 3) if avg_hit_rate is not None else "N/A",
                "avg_agreement_rate": round(avg_agreement, 3),
                "fail_rate": round(fail_rate, 3),
            },
            "thresholds": RELEASE_GATE_CONFIG,
            "checks": checks,
            "cost_summary": self.cost_tracker.get_summary(),
        }
```

---

## 💻 Bước 3: Cập nhật `main.py` — Thêm Release Gate Report

Tìm và thêm vào cuối hàm `main()` trong `main.py`:

```python
# Sau khi in V1 và V2 scores, thêm Release Gate Report:

# Kiểm tra Release Gate từ runner
gate_result = runner.check_release_gate(v2_results)
print("\n🚦 --- RELEASE GATE REPORT ---")
print(f"Quyết định: {gate_result['decision']}")
print(f"Avg Score: {gate_result['metrics']['avg_score']} (min: {gate_result['thresholds']['min_avg_score']})")
print(f"Hit Rate: {gate_result['metrics']['avg_hit_rate']} (min: {gate_result['thresholds']['min_hit_rate']})")
print(f"Agreement: {gate_result['metrics']['avg_agreement_rate']}")
print(f"Fail Rate: {gate_result['metrics']['fail_rate']}")
print(f"\n💰 Chi phí: ${gate_result['cost_summary']['estimated_cost_usd']} USD")
print(f"   Tổng tokens: {gate_result['cost_summary']['total_tokens']:,}")
```

---

## 🧪 Bước 4: Kiểm tra

```powershell
# Kiểm tra syntax
python -c "
import ast
for f in ['engine/runner.py']:
    with open(f) as fp:
        ast.parse(fp.read())
    print(f'✅ {f}: Syntax OK')
"

# Test nhanh CostTracker
python -c "
from engine.runner import CostTracker, RELEASE_GATE_CONFIG
tracker = CostTracker()
tracker.record_call('gpt-4o', 500, 100)
tracker.record_call('gemini-2.5-pro', 500, 100)
summary = tracker.get_summary()
print('Total calls:', summary['total_api_calls'])
print('Cost USD:', summary['estimated_cost_usd'])
print('RELEASE_GATE_CONFIG:', RELEASE_GATE_CONFIG)
"
```

**Output kỳ vọng:**
```
✅ engine/runner.py: Syntax OK
Total calls: 2
Cost USD: 0.0025 (khoảng)
RELEASE_GATE_CONFIG: {'min_avg_score': 3.5, ...}
```

---

## 💾 Bước 5: Commit

```powershell
git add engine/runner.py main.py

git commit -m "feat: async BenchmarkRunner với CostTracker và Release Gate

- Implement BenchmarkRunner hoàn toàn async (asyncio.gather per batch)
- Thêm CostTracker: tracking token usage và chi phí USD
- Batch processing với configurable delay giữa batches (tránh rate limit)
- Xử lý lỗi riêng từng test case (không crash toàn bộ pipeline)
- check_release_gate(): tự động quyết định APPROVE/BLOCK dựa trên ngưỡng
- Cập nhật main.py hiển thị Release Gate Report đầy đủ"

git push origin feature/minh-async-runner
```

---

## 🔗 Bước 6: Tạo Pull Request

1. Vào GitHub repo
2. Click **"Compare & pull request"**
3. Điền:
   - **Title:** `[Minh] feat: Async BenchmarkRunner với Cost Tracking và Release Gate`
   - **Description:**
     ```
     ## Những gì đã làm
     - Hoàn thiện engine/runner.py: async pipeline với batch processing
     - CostTracker: theo dõi GPT-4o + Gemini token & chi phí USD
     - RELEASE_GATE_CONFIG: ngưỡng tự động APPROVE/BLOCK
     - check_release_gate(): tổng hợp metrics và ra quyết định
     - Xử lý exception riêng cho từng test case
     
     ## Performance
     - 50 cases với batch_size=5: ~X phút
     - Chi phí ước tính: $X.XX/run
     
     ## Release Gate
     - min_avg_score: 3.5/5.0
     - min_hit_rate: 0.7
     - max_fail_rate: 0.3
     
     ## Cách kiểm tra
     python -c "from engine.runner import CostTracker; ..."
     ```
4. **Reviewer: Trung**
5. Click **"Create Pull Request"**

---

## ⚠️ Những Điểm Kỹ Thuật Cần Hiểu

| Khái niệm | Giải thích |
|-----------|-----------|
| **asyncio.gather** | Chạy nhiều coroutine cùng lúc — nhanh hơn chạy tuần tự |
| **batch_size** | Giới hạn số case chạy song song — tránh API bị overload / rate limit |
| **Release Gate** | Ngưỡng chất lượng tối thiểu: nếu V2 không đạt → bị block (không deploy) |
| **Cost tracking** | Theo dõi token usage → tính chi phí API thực tế |
| **return_exceptions=True** | asyncio.gather không crash khi 1 task lỗi — trả về Exception thay thế |

---

*File này được tạo bởi Coding Agent cho Minh — Lab 14 AI Evaluation Factory*
