# Walkthrough — Lab 14: AI Evaluation Factory

Dự án này thực hiện xây dựng một quy trình đánh giá (Evaluation Pipeline) toàn diện cho hệ thống RAG phục vụ môn học C/C++. 

## 🎯 Mục tiêu
- Xây dựng bộ dataset "Golden Set" chất lượng cao (162 cases).
- Triển khai cơ chế Multi-Judge (Cloud-based) để đạt độ chính xác tối đa.
- Tự động hóa việc đo lường các chỉ số: **Hit Rate, MRR, Accuracy, Latency, Cost**.

## 🛠️ Các thành phần cốt lõi

### 1. Dataset Enrichment (SDG)
Chúng tôi đã mở rộng bộ dataset ban đầu lên **162 cases** bao gồm:
- **Factual questions:** Kiểm tra kiến thức cơ bản.
- **Debug/Coding questions:** Kiểm tra khả năng hiểu code C.
- **Adversarial/Out-of-range:** Thách thức khả năng từ chối của Assistant.

### 2. Multi-Judge Architecture
Hệ thống sử dụng bộ đôi giám khảo Cloud-only thế hệ mới nhất:
- **Judge 1:** `gpt-4o-mini` - Đánh giá tốc độ và độ chính xác cơ bản.
- **Judge 2:** `gpt-5.4-mini` - Xử lý các lập luận phức tạp và logic lập trình.
- **Consensus Logic:** Tự động tính toán tỷ lệ đồng thuận và phát hiện xung đột để con người review.

### 3. High-Performance Runner
- **Async Processing:** Xử lý song song theo batch để tối ưu API throughput.
- **Auto-Retry & Rate Limit Protection:** Tự động parse thời gian chờ từ API OpenAI và thử lại, đảm bảo 100% hoàn thành task.
- **Cost Tracking:** Theo dõi chi phí thực tế theo từng token của từng model.

## 📊 Kết quả cuối cùng (V2 Production)

| Metric | Giá trị | Trạng thái |
|--------|---------|------------|
| **Average Score** | **4.75 / 5.0** | ✅ Vượt V1 (3.8) |
| **Hit Rate @3** | **100%** | ✅ Tuyệt đối |
| **MRR** | **1.0** | ✅ Tuyệt đối |
| **Judge Agreement** | **90.0%** | ✅ Rất cao |
| **Pass Rate** | **96.9%** | ✅ Tin cậy |
| **Total Cost** | **$0.171** | ✅ Siêu tiết kiệm |

## 🚀 Kết luận & Quyết định
Dựa trên delta performance **+0.95**, hệ thống đã vượt qua bài kiểm tra Regression Test một cách xuất sắc. 

**QUYẾT ĐỊNH: RELEASE APPROVED (GATE PASSED)**.

---
