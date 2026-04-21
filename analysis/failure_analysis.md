# Failure Analysis — Lab 14 Benchmarking

## 📊 Evaluation Summary
*Tóm tắt kết quả từ reports/summary.json*
- **Total Cases:** 162
- **Pass Rate:** XX%
- **Avg Score:** X.X/5.0
- **Hit Rate @3:** 0.XX
- **MRR:** 0.XX

---

## 🔍 Deep Dive: Root Cause Analysis (5 Whys)

*Chọn ra 1-2 cases "Worst" (điểm thấp nhất) để phân tích sâu.*

### Case #1: [Tóm tắt câu hỏi]
- **Symptom:** Agent trả lời sai/thiếu thông tin/hallucination.
- **Why 1:** Tại sao Agent trả lời sai?
  - *Ví dụ: Vì RAG không tìm được tài liệu liên quan.*
- **Why 2:** Tại sao RAG không tìm được tài liệu?
  - *Ví dụ: Vì câu hỏi chứa thuật ngữ không có trong index.*
- **Why 3:** Tại sao thuật ngữ đó không có trong index?
  - *Ví dụ: Vì chúng ta chunk quá nhỏ làm mất tính ngữ nghĩa (semantic context).*
- **Why 4:** Tại sao chunk quá nhỏ?
  - *Ví dụ: Vì config.py đặt CHUNK_SIZE=512 để tối ưu latency.*
- **Why 5 (Root Cause):** Gốc rễ vấn đề là gì?
  - *Ví dụ: Thiếu bước Keyword Extraction hoặc HyDE để mở rộng câu hỏi trước khi search.*

---

## 💡 Retrieval vs. Answer Quality Correlation
*Giải trình sự liên quan giữa chất lượng Retrieval và chất lượng câu trả lời (Tiêu chí Rubric).*

- **Phân tích:** Khi Hit Rate giảm xuống dưới X%, điểm Accuracy của Judge thường giảm theo tỉ lệ thuận Y%...
- **Kết luận:** RAG là "móng nhà", nếu RAG tìm sai thì LLM Judge dù thông minh đến đâu cũng không thể cứu được câu trả lời.

---

## 🛠️ Action Plan cho V3
1. ...
2. ...
