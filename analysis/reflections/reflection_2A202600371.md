# 🚀 Lab Day 14: AI Evaluation Factory - Reflection

**Họ và tên:** Hoàng Đức Nghĩa <br>
**Mã sinh viên:** 2A202600371<br>
**Vai trò:** Contributor — Thiết lập Golden Dataset thủ công<br>
**Ngày nộp:** 15/04/2026

## 1. Tôi phụ trách phần nào?

**File / module:**

- `data/golden_set.jsonl` (Tạo 60 test case thủ công, chất lượng cao cho golden dataset)

**Kết nối với thành viên khác:**

Tôi phối hợp với nhóm để tạo **bộ dữ liệu kiểm tra thủ công (Golden Dataset)** cho hệ thống benchmark, bao gồm **60 test cases thủ công** với chất lượng cao, format chuẩn JSONL để hệ thống đọc được và bao gồm đủ các loại câu hỏi. Công việc của tôi đảm bảo rằng cả nhóm có data để develop Eval Engine và Async Runner

**Bằng chứng (commit / comment trong code):**

Commit "feat: tạo 60 test cases thủ công cho golden dataset- 15 câu factual (con trỏ, mảng, vòng lặp, printf, deadline)- 15 câu debug (segmentation fault, struct vs class)- 15 câu adversarial (ngoài phạm vi, vi phạm học thuật)- 15 câu về grading policy" trong nhánh `feature/nghia-golden dataset`
Hoạt động của tôi thể hiện qua chỉnh sửa `data/golden_set.jsonl`

---

## 2. Công việc đã làm 

Tôi tạo file `data/golden_set.jsonl` với nội dung sau:
- 60 test case thủ công chất lượng cao
- Format chuẩn JSONL để hệ thống đọc được: {"question": , "expected_answer": , "context": , "difficulty": , "type": , "expected_retrieval_ids": []}
- Bao gồm 4 loại câu hỏi: factual, debug, adversarial và grading policy; 15 câu mỗi loại để tránh bias

---

## 3. Kỹ thuật 

- Tôi tạo 60 test case thủ công sao cho các câu hỏi giống với những câu hỏi mà tôi và những sinh viên khác hay hỏi chatbot
- MRR (Mean Reciprocal Rank): đánh giá khả năng retrieval đúng
- Cohen’s Kappa: đo độ đồng thuận giữa người chấm và model
- Position Bias: bias khi model ưu tiên thông tin ở vị trí đầu
- Hiểu về trade-off giữa Chi phí và Chất lượng: Muốn Eval Engine tốt hơn thì Golden dataset cần phải có chất lượng tốt hơn: nhiều test case hơn, test case bao quát nhiều trường hợp hơn, test case giống với các câu hỏi thực tế hơn, ... Và muốn thế thì cần phải tốn nhiều thời gian và resource hơn để tạo dataset. Đương nhiên không phải chỉ cần dataset có chi phí cao là nó là dataset tốt, mà chúng ta cần phải kiểm tra rằng dataset đó nó đáp ứng yêu cầu không đã.

---

## 4. Lỗi đã bắt gặp

- Một số câu adversarial trả lời chưa đủ “refuse đúng chuẩn AI TA”
- Một số câu mang tính textbook, chưa giống cách sinh viên thật sự hỏi
- Sai format json: Có vài câu bị xuống dòng giữa JSON

---

## 5. Cách sửa lỗi 

- Chuẩn hóa expected_answer :<br>
    Adversarial → từ chối + offer help<br>
    Grading → redirect LMS<br>
    Debug → giải thích nguyên nhân + ví dụ
- Cải thiện chất lượng câu hỏi : Tôi viết lại các câu hỏi theo cách sinh viên hay hỏi như “code em bị lỗi…”, “deadline khi nào…”, ...
- Tôi check lại bằng code xem đủ 60 cases chưa, nếu chưa thì tôi kiểm tra lại xem question nào bị sai format

---

## 6. Bài học rút ra

- Data quan trọng không kém model: Nếu Model tốt nhưng dataset kém thì evaluation vẫn bị sai hoàn toàn
- Cần thiết kế dataset có chủ đích: Dataset không được random, mà các test case phải đúng, cover đủ scenario, tránh bias
- AI TA không chỉ trả lời đúng mà phải biết trả lời “đúng vai trò”: Biết từ chối khi cần, không vi phạm academic integrity
- Validation là bắt buộc: Chỉ cần sai 1 dòng JSONL → pipeline fail

---

## 7. Cải tiến tiếp theo 
Nếu có thêm thời gian, tôi sẽ cải thiện phần của mình bằng cách gắn nhãn chi tiết hơn: Tôi sẽ thêm metadata như skill: pointer / array / loop / memory, intent: hỏi lý thuyết / debug / xin lời giải, ... để giúp phân tích performance model sâu hơn.

