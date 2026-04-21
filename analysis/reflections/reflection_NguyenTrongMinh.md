# 📝 Báo Cáo Cá Nhân — Lab 14: AI Evaluation Factory

> **Họ tên:** Minh  
> **Vai trò:** Async Benchmark Runner + Cost Tracking  
> **Nhánh Git:** `feature/minh-async-runner`  
> **Ngày nộp:** 21/04/2026  

---

## 1. Đóng Góp Kỹ Thuật (Engineering Contribution)

### 1.1 Những gì tôi đã xây dựng

Tôi chịu trách nhiệm hoàn thiện **`engine/runner.py`** và cập nhật **`main.py`**, đây là thành phần "xương sống" quyết định toàn bộ pipeline đánh giá có chạy được song song và nhanh hay không.

**Module `CostTracker`**

Tôi thiết kế class `CostTracker` để theo dõi toàn bộ chi phí API trong suốt quá trình benchmark. Mỗi lần một model Judge được gọi, tracker ghi nhận số `input_tokens`, `output_tokens`, rồi tính ra chi phí USD dựa trên bảng giá thực tế (GPT-4o: \$2.50/1M input, \$10.00/1M output; Gemini-2.5-Pro: \$1.25/1M input, \$5.00/1M output). Kết quả cuối được tổng hợp qua `get_summary()`, bao gồm tổng số API calls, tổng tokens, chi phí ước tính, và **chi phí trung bình mỗi test case**.

```python
def record_call(self, model: str, input_tokens: int, output_tokens: int) -> None:
    ...
    cost = (input_tokens * self.GPT4O_INPUT_PRICE / 1_000_000 +
            output_tokens * self.GPT4O_OUTPUT_PRICE / 1_000_000)
    self.estimated_cost_usd += cost
```

**Module `BenchmarkRunner` — Async Pipeline**

Đây là phần kỹ thuật phức tạp nhất. Tôi triển khai pipeline 4 bước cho từng test case:

1. **Gọi Agent** (`await self.agent.query(question)`) — hoàn toàn async, không có blocking call
2. **Tính Retrieval Metrics** — gọi `RetrievalEvaluator` để tính Hit Rate và MRR
3. **Chạy Multi-Judge** — gọi `judge.evaluate_multi_judge()` song song 2 model (strict + lenient)
4. **Xác định trạng thái pass/fail** dựa trên ngưỡng `RELEASE_GATE_CONFIG`

Điểm then chốt là hàm `run_dataset()` dùng `asyncio.gather(*tasks, return_exceptions=True)` để chạy toàn bộ một batch song song. Với `batch_size=5` và `delay_between_batches=1s`, pipeline đảm bảo không bị rate limit trong khi vẫn tận dụng tối đa concurrency.

**Module `check_release_gate()`**

Hàm này tổng hợp metrics từ tất cả valid results, so sánh với 4 ngưỡng trong `RELEASE_GATE_CONFIG`, và tự động ra quyết định **APPROVE** hoặc **BLOCK RELEASE**:

| Chỉ số | Ngưỡng tối thiểu | Kết quả thực tế (V2) |
|--------|:----------------:|:-------------------:|
| Avg Score | ≥ 3.5 / 5.0 | **4.88** ✅ |
| Hit Rate | ≥ 0.7 | **1.0** ✅ |
| Agreement Rate | ≥ 0.6 | **0.9** ✅ |
| Fail Rate | ≤ 0.3 | **~0.1** ✅ |

**Kết quả Release Gate: ✅ APPROVE**

**Cập nhật `main.py`**

Tôi thêm phần in Release Gate Report vào cuối `main()`, hiển thị đầy đủ decision, từng chỉ số so với ngưỡng, và báo cáo chi phí tổng:

```python
gate_result = runner.check_release_gate(v2_results)
print(f"Quyết định: {gate_result['decision']}")
print(f"💰 Chi phí: ${gate_result['cost_summary']['estimated_cost_usd']} USD")
```

### 1.2 Git Workflow

- Tạo nhánh `feature/minh-async-runner` từ `main`
- Commit với message chi tiết mô tả từng thay đổi
- Tạo Pull Request, assign reviewer là Trung
- Merge vào `main` sau khi pass code review

---

## 2. Chiều Sâu Kỹ Thuật (Technical Depth)

### 2.1 Mean Reciprocal Rank (MRR) là gì?

MRR đo lường **trung bình vị trí đầu tiên** mà tài liệu đúng xuất hiện trong danh sách retrieved chunks. Công thức:

$$MRR = \frac{1}{|Q|} \sum_{i=1}^{|Q|} \frac{1}{\text{rank}_i}$$

Ví dụ: nếu tài liệu đúng xuất hiện ở vị trí 1 → MRR = 1.0; vị trí 2 → MRR = 0.5; vị trí 3 → MRR = 0.33.

Trong benchmark này, hệ thống đạt **MRR = 1.0** trên toàn bộ valid cases, có nghĩa là tài liệu đúng **luôn xuất hiện ở vị trí số 1** trong danh sách retrieved. Đây là kết quả lý tưởng, chứng minh Retrieval stage hoạt động cực tốt trước khi sang Generation.

**Mối liên hệ giữa Retrieval Quality và Answer Quality:** Nếu Retrieval sai (tài liệu không liên quan), thì dù Judge có tốt đến mấy, Agent vẫn sẽ hallucinate. MRR = 1.0 là điều kiện cần thiết để đảm bảo câu trả lời có cơ sở.

### 2.2 Cohen's Kappa — Đo lường độ đồng thuận thực sự

Agreement Rate đơn thuần (tỷ lệ % hai judge cho cùng điểm) có một điểm yếu: nó không loại trừ khả năng hai judge vô tình đồng ý do ngẫu nhiên. **Cohen's Kappa** khắc phục điều đó:

$$\kappa = \frac{P_o - P_e}{1 - P_e}$$

Trong đó $P_o$ là agreement rate thực tế, $P_e$ là xác suất đồng ý do ngẫu nhiên. Kappa = 1.0 là đồng thuận hoàn hảo; Kappa ≈ 0 là chỉ do may mắn.

Hệ thống của nhóm hiện dùng Agreement Rate = 0.9, là một chỉ số tốt nhưng chưa tính đến yếu tố ngẫu nhiên. Trong production, nên thay thế bằng Cohen's Kappa để có con số đáng tin cậy hơn.

### 2.3 Position Bias trong LLM Judge

**Position Bias** là hiện tượng LLM Judge có xu hướng ưu tiên câu trả lời xuất hiện ở một vị trí nhất định (thường là vị trí đầu tiên trong prompt) dù nội dung không tốt hơn. Đây là lý do tại sao chỉ dùng 1 Judge đơn lẻ là rủi ro.

Hệ thống của nhóm dùng 2 Judge với hệ thống prompt **khác nhau** (strict vs lenient), giúp triệt tiêu một phần bias. Để kiểm soát tốt hơn, có thể dùng kỹ thuật **swap position**: đổi thứ tự đặt `expected_answer` và `agent_response` trong prompt rồi so sánh kết quả.

### 2.4 Trade-off giữa Chi phí và Chất lượng

Từ dữ liệu benchmark thực tế:

| Thành phần | Chi phí ước tính / case | Chất lượng |
|-----------|:-----------------------:|:----------:|
| GPT-4o Judge | ~\$0.000150 | Strict, chính xác cao |
| Gemini-2.5-Pro Judge | ~\$0.000075 | Cân bằng, nhanh hơn |
| Cả 2 Judge | ~\$0.000225 | Độ tin cậy cao nhất |

Với 100 cases/run, tổng chi phí khoảng **\$0.02 — hoàn toàn chấp nhận được**. Nếu cần cắt 30% chi phí mà không giảm độ chính xác, có thể áp dụng chiến lược **tiered evaluation**: chỉ dùng 1 Judge cho những case có confidence cao (score 1 hoặc 5), dùng cả 2 Judge cho những case có score ở mức trung bình (2–4) — vì đây là những case dễ xung đột nhất.

---

## 3. Giải Quyết Vấn Đề (Problem Solving)

### Vấn đề 1: Pipeline crash khi một test case lỗi

**Triệu chứng:** Khi chạy `asyncio.gather()` mà không có xử lý lỗi, nếu một task ném exception, toàn bộ batch bị crash và không có kết quả nào được lưu.

**Giải pháp:** Dùng tham số `return_exceptions=True` trong `asyncio.gather()`. Khi đó, các exception không lan rộng mà được trả về như một giá trị bình thường trong list kết quả. Sau đó kiểm tra `isinstance(result, Exception)` để xử lý riêng từng case lỗi và gán `status = "error"` thay vì crash.

```python
batch_results = await asyncio.gather(*tasks, return_exceptions=True)
for result in batch_results:
    if isinstance(result, Exception):
        results.append({"status": "error", "error": str(result), ...})
    else:
        results.append(result)
```

### Vấn đề 2: API Rate Limit khi chạy quá nhiều request cùng lúc

**Triệu chứng:** Chạy song song 40 cases cùng lúc → API trả về lỗi 429 (Too Many Requests).

**Giải pháp:** Chia dataset thành các batch nhỏ (`batch_size=5`), mỗi batch chạy song song bên trong, nhưng giữa các batch có `await asyncio.sleep(delay_between_batches)`. Cách này cân bằng giữa tốc độ (concurrency trong batch) và tuân thủ rate limit (delay giữa batches).

### Vấn đề 3: Không có expected_retrieval_ids ở một số test cases

**Triệu chứng:** Một số test cases trong golden dataset không có field `expected_retrieval_ids`, khiến việc tính Hit Rate và MRR bị lỗi `KeyError`.

**Giải pháp:** Thêm guard check trước khi tính retrieval metrics:

```python
expected_ids = test_case.get("expected_retrieval_ids", [])
if expected_ids:
    hit_rate = self.retrieval_eval.calculate_hit_rate(...)
    mrr = self.retrieval_eval.calculate_mrr(...)
else:
    hit_rate = None
    mrr = None
```

Khi tổng hợp trong `check_release_gate()`, lọc ra chỉ những case có `hit_rate is not None` để tính trung bình, tránh sai lệch kết quả.

---

## 4. Kết luận

Qua Lab 14, tôi hiểu rõ hơn rằng việc xây dựng một hệ thống đánh giá AI không chỉ là "gọi một model để chấm điểm model khác". Độ tin cậy đến từ nhiều lớp: Retrieval phải đúng trước (MRR), Judge phải khách quan và đồng thuận với nhau (Agreement Rate / Cohen's Kappa), pipeline phải chịu được lỗi mà không crash, và chi phí phải được theo dõi và tối ưu.

Phần tôi tự tin nhất là thiết kế **Release Gate logic** — đây là thứ mà trong production thực tế, quyết định có deploy phiên bản mới hay không đều phải dựa trên các ngưỡng rõ ràng như vậy, thay vì phán đoán thủ công.

Điều tôi muốn cải thiện thêm nếu có thêm thời gian: thay Agreement Rate bằng **Cohen's Kappa**, và thêm **swap-position test** để phát hiện Position Bias trong Judge.