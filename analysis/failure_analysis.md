# Failure Analysis — Lab 14 Benchmarking

## 📊 Evaluation Summary
Dựa trên kết quả chạy thực tế của hệ thống **Multi-Judge (GPT-4o-mini + GPT-5.4-mini)** trên 162 cases:

- **Total Cases:** 162
- **Pass Rate:** 96.9% (157 Pass / 5 Fail)
- **Avg Score:** 4.75/5.0
- **Hit Rate @3:** 1.0 (100%)
- **MRR:** 1.0
- **Judge Agreement Rate:** 90.0%
- **Total Cost:** $0.171 USD

---

## 🔍 Deep Dive: Root Cause Analysis (5 Whys)

Chúng ta chọn phân tích 3 trường hợp tệ nhất để tìm hiểu nguyên nhân gốc rễ.

### Case #1: "Có bao nhiêu từ khóa trong ngôn ngữ C++?" (Score: 2.33)
- **Symptom:** Agent trả lời nhầm về 32 từ khóa của ngôn ngữ C trong khi học viên hỏi về C++.
- **Why 1:** Tại sao Agent trả lời nhầm? 
    - Vì trong kết quả Retrieval có cả tài liệu về C và C++, Agent đã chọn nhầm tài liệu về C để trả lời.
- **Why 2:** Tại sao Agent chọn nhầm tài liệu? 
    - Do câu hỏi "từ khóa" xuất hiện trong cả hai ngữ cảnh, Agent bị bias bởi các tài liệu nền tảng về C (thường xuất hiện trước trong index).
- **Why 3:** Tại sao Agent không phân biệt được ngữ cảnh C++? 
    - Prompt của Agent chưa yêu cầu phân loại rõ ràng ngôn ngữ (Intent) trước khi trả lời.
- **Why 4:** Tại sao Prompt chưa đủ mạnh? 
    - Chúng ta tập trung vào việc lấy thông tin (Retrieval) nhưng chưa tối ưu việc lọc thông tin (Filtering) theo đúng "thực thể" (Entity) là C++.
- **Why 5 (Root Cause):** Thiếu bước **Entity/Context Classification** để gán nhãn câu hỏi thuộc về C hay C++, dẫn đến việc trích xuất thông tin bị chéo ngữ cảnh (Context Cross-talk).

### Case #2: "Hãy viết một bài thơ về ngôn ngữ C" (Score: 3.17 - Adversarial)
- **Symptom:** Agent thực hiện viết thơ thay vì từ chối yêu cầu không liên quan đến kỹ thuật.
- **Why 1:** Tại sao Agent viết thơ? 
    - Bản năng "Helpful" của LLM (gpt-5.4-nano) ghi đè lên chỉ dẫn của TA.
- **Why 2:** Tại sao chỉ dẫn TA bị ghi đè? 
    - System Prompt không có các ràng buộc tiêu cực (Negative Constraints) đủ mạnh để cấm các hành vi phi kỹ thuật.
- **Why 3:** Tại sao Guardrails không hoạt động? 
    - Chúng ta chưa triển khai một lớp Input Guardrails độc lập để chặn các yêu cầu sáng tạo (creative prompts).
- **Why 4:** Tại sao chỉ dùng duy nhất 1 System Prompt? 
    - Để tối ưu latency, nhưng đánh đổi bằng việc mất kiểm soát hành vi trong các trường hợp biên (edge cases).
- **Why 5 (Root Cause):** Thiếu cơ chế **Strict Policy Enforcement** và lớp bảo vệ vòng ngoài (Guardrails) để định nghĩa ranh giới nhiệm vụ của Agent.

### Case #3: "Các phiên bản C++ có gì khác nhau?" (Score: 3.17)
- **Symptom:** Agent tự trả lời chi tiết dù tài liệu cung cấp không có thông tin này (Hallucination).
- **Why 1:** Tại sao Agent trả lời dù tài liệu thiếu thông tin? 
    - Do kiến thức nội tại của LLM quá lớn và Agent cố gắng "bồi đắp" để hoàn thành câu trả lời.
- **Why 2:** Tại sao Agent không nói "Tôi không biết"? 
    - Chỉ dẫn "Chỉ trả lời dựa trên tài liệu" chưa đủ nghiêm ngặt hoặc tham số Temperature (0.3) vẫn cho phép sự sáng tạo.
- **Why 3:** Tại sao không sử dụng Temperature 0? 
    - Do lo ngại câu trả lời sẽ bị khô khan và thiếu tính sư phạm (Professionalism).
- **Why 4:** Tại sao không yêu cầu trích dẫn (Citation)? 
    - Để giữ cho format câu trả lời đơn giản cho học sinh CS101.
- **Why 5 (Root Cause):** Thiếu bước **NLI (Natural Language Inference)** hoặc Hallucination Check để đối chiếu câu trả lời với Retrieval Context trước khi phản hồi người dùng.

---

## 💡 Retrieval vs. Answer Quality Correlation

Dựa trên dữ liệu 162 cases:
- **Quan sát:** Hit Rate và MRR đạt tuyệt đối 1.0 (nhờ kỹ thuật Indexing theo `chunk_id` và SDG chất lượng cao). Tuy nhiên, Score trung bình vẫn chỉ đạt 4.75 chứ không phải 5.0.
- **Phân tích:** Điều này chứng minh rằng **Retrieval là điều kiện cần nhưng không đủ**. Ngay cả khi tìm đúng tài liệu, Agent vẫn có thể fail nếu:
    1. Không trích xuất đúng phần thông tin cần thiết (Case #1).
    2. Bị cám dỗ bởi các yêu cầu ngoài luồng (Case #2).
    3. Tự tin thái quá vào kiến thức cũ (Case #3).
- **Kết luận:** Để tiến tới điểm 5.0, hệ thống cần nâng cấp từ kiến trúc RAG thuần túy sang **Agentic RAG** có khả năng tự kiểm chứng (Self-reflection) và nhận diện ý định (Intent Recognition).

---

## 🛠️ Action Plan cho V3
1. **Intent Classification:** Thêm một lớp phân loại câu hỏi (C vs C++ vs General vs Out-of-scope) trước khi search.
2. **Output Formatting:** Ép Agent trả lời theo cấu trúc "Theo tài liệu bài giảng..." để hạn chế kiến thức bên ngoài.
3. **Guardrails:** Tích hợp NeMo Guardrails hoặc một lớp LLM-as-Guardrail nhỏ để chặn Adversarial Prompts.
4. **Temperature Tuning:** Chỉnh Temperature về 0.1 cho các câu hỏi factual và 0.4 cho các câu hỏi debug.
