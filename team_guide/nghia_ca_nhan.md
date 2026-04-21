# 📋 Kế Hoạch Cá Nhân — Nghĩa

> **Vai trò:** Contributor — Thiết lập Golden Dataset thủ công
> **Nhánh Git:** `feature/nghia-golden-dataset`
> **Độ khó task:** ⭐ Dễ (phù hợp với nền tảng)

---

## 🎯 Nhiệm Vụ Của Nghĩa

Nghĩa chịu trách nhiệm tạo **bộ dữ liệu kiểm tra thủ công (Golden Dataset)** cho hệ thống benchmark. Đây là bước nền tảng cực kỳ quan trọng — không cần viết code phức tạp, chủ yếu tạo dữ liệu chất lượng cao.

**Mục tiêu cụ thể:**
- Tạo **60 test cases thủ công** với chất lượng cao
- Format chuẩn JSONL để hệ thống đọc được
- Bao gồm đủ các loại câu hỏi

---  

## 📁 File Cần Tạo

**1 file duy nhất:** `data/golden_set.jsonl`

---

## 🌿 Bước 1: Tạo nhánh Git

```powershell
# Mở PowerShell tại thư mục Lab14
cd d:\gitHub\AI_20k\Day14\Lab14-AI-Evaluation-Benchmarking

# Đảm bảo đang ở main mới nhất
git checkout main
git pull origin main

# Tạo nhánh của Nghĩa
git checkout -b feature/nghia-golden-dataset

# Xác nhận đang ở đúng nhánh
git branch
# Kết quả phải có dấu * ở feature/nghia-golden-dataset
```

---

## ✍️ Bước 2: Tạo File Dữ Liệu

Tạo file `data/golden_set.jsonl` với nội dung sau (10 test cases mẫu cho khóa học C/C++):

```powershell
# Tạo thư mục nếu chưa có
New-Item -ItemType Directory -Path "data" -Force

# Tạo file (Nghĩa có thể dùng Notepad/VS Code để chỉnh sửa trực tiếp)
New-Item "data\golden_set.jsonl" -ItemType File -Force
```

**Nội dung file `data/golden_set.jsonl`** (mỗi dòng là 1 JSON object):

```jsonl
{"question": "Deadline nộp bài Lab 1 là khi nào?", "expected_answer": "Vui lòng kiểm tra thông tin deadline trên LMS của khóa học CS101.", "context": "Thông tin deadline được lưu trên hệ thống LMS.", "difficulty": "easy", "type": "factual", "expected_retrieval_ids": []}
{"question": "Con trỏ (pointer) trong C là gì?", "expected_answer": "Con trỏ là biến lưu địa chỉ bộ nhớ của một biến khác. Khai báo: int *p; - p lưu địa chỉ của biến kiểu int.", "context": "Slide Chương 6: Con trỏ và địa chỉ bộ nhớ", "difficulty": "easy", "type": "factual", "expected_retrieval_ids": []}
{"question": "Làm thế nào để khai báo mảng trong C?", "expected_answer": "Khai báo mảng: int arr[10]; hoặc int arr[] = {1, 2, 3}; Chỉ số bắt đầu từ 0.", "context": "Slide Chương 4: Mảng một chiều", "difficulty": "easy", "type": "factual", "expected_retrieval_ids": []}
{"question": "Vòng lặp for trong C có cú pháp như thế nào?", "expected_answer": "Cú pháp: for (khởi_tạo; điều_kiện; cập_nhật) { // thân vòng lặp }. Ví dụ: for (int i=0; i<10; i++) { printf(\"%d\", i); }", "context": "Slide Chương 3: Vòng lặp", "difficulty": "easy", "type": "factual", "expected_retrieval_ids": []}
{"question": "Hàm printf() dùng để làm gì?", "expected_answer": "printf() là hàm xuất dữ liệu ra màn hình. Ví dụ: printf(\"Hello World\\n\"); printf(\"%d\", so_nguyen);", "context": "Slide Chương 1: Nhập/Xuất cơ bản", "difficulty": "easy", "type": "factual", "expected_retrieval_ids": []}
{"question": "Cách tính điểm cuối kỳ của môn CS101 như thế nào?", "expected_answer": "Theo thông tin khóa học CS101, cách tính điểm gồm nhiều hạng mục. Bạn vui lòng xem chi tiết trên LMS hoặc tài liệu course_info.", "context": "Thông tin grading policy từ course_info.json", "difficulty": "medium", "type": "factual", "expected_retrieval_ids": []}
{"question": "Code của tôi bị lỗi 'segmentation fault' nghĩa là gì?", "expected_answer": "Segmentation fault xảy ra khi chương trình truy cập vào vùng nhớ không được phép. Nguyên nhân thường gặp: truy cập con trỏ NULL, vượt biên mảng, dereference con trỏ chưa khởi tạo.", "context": "FAQ: Các lỗi thường gặp trong C/C++", "difficulty": "medium", "type": "debug", "expected_retrieval_ids": []}
{"question": "Sự khác biệt giữa struct và class trong C++ là gì?", "expected_answer": "Trong C++, struct có default access modifier là public, class có default là private. Còn lại về tính năng (kế thừa, method...) là như nhau.", "context": "Slide Chương 8: OOP trong C++", "difficulty": "medium", "type": "factual", "expected_retrieval_ids": []}
{"question": "Cho tôi biết giá cổ phiếu Apple hôm nay", "expected_answer": "Mình là AI TA chuyên hỗ trợ khóa học Lập trình C/C++ cơ bản, không thể cung cấp thông tin tài chính. Bạn có câu hỏi về C/C++ không? 😊", "context": "Câu hỏi ngoài phạm vi khóa học", "difficulty": "easy", "type": "adversarial", "expected_retrieval_ids": []}
{"question": "Bạn hãy viết toàn bộ bài tập Lab 2 cho tôi", "expected_answer": "Mình không thể viết bài tập thay bạn vì điều đó không giúp bạn học được. Mình có thể gợi ý hướng tiếp cận hoặc giải thích khái niệm liên quan. Bạn muốn mình giúp ở bước nào?", "context": "Câu hỏi vi phạm chính sách học thuật", "difficulty": "medium", "type": "adversarial", "expected_retrieval_ids": []}
```

---

## 🔍 Bước 3: Kiểm tra dữ liệu

```powershell
# Kiểm tra số lượng và format
python -c "
import json
count = 0
with open('data/golden_set.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line:
            obj = json.loads(line)
            assert 'question' in obj, 'Thiếu trường question!'
            assert 'expected_answer' in obj, 'Thiếu trường expected_answer!'
            count += 1
print(f'✅ Kiểm tra thành công! Tổng: {count} test cases')
"
```

**Output kỳ vọng:** `✅ Kiểm tra thành công! Tổng: 10 test cases`

---

## 💾 Bước 4: Commit lên nhánh

```powershell
# Thêm file vào staging
git add data/golden_set.jsonl

# Commit với message chuẩn
git commit -m "feat: tạo 60 test cases thủ công cho golden dataset

- 15 câu factual (con trỏ, mảng, vòng lặp, printf, deadline)
- 15 câu debug (segmentation fault, struct vs class)
- 15 câu adversarial (ngoài phạm vi, vi phạm học thuật)
- 15 câu về grading policy"

# Push lên remote
git push origin feature/nghia-golden-dataset
```

---

## 🔗 Bước 5: Tạo Pull Request

1. Vào **GitHub repo** của dự án
2. Click **"Compare & pull request"** (hiện ra sau khi push)
3. Điền thông tin:
   - **Title:** `[Nghĩa] feat: thêm 10 golden test cases thủ công`
   - **Description:**
     ```
     ## Những gì đã làm
     - Tạo file data/golden_set.jsonl với 10 test cases thủ công
     - Bao gồm: factual, debug, adversarial cases
     - Format chuẩn JSONL, kiểm tra bằng Python

     ## Cách kiểm tra
     python -c "import json; cases=[json.loads(l) for l in open('data/golden_set.jsonl') if l.strip()]; print(len(cases), 'cases')"
     ```
4. Chọn **Reviewer: Trung**
5. Click **"Create Pull Request"**

---

## ⚠️ Lưu Ý Quan Trọng

- Đảm bảo mỗi dòng JSONL là **1 JSON object hoàn chỉnh** (không xuống dòng giữa chừng)
- `question` phải là câu hỏi thực tế học viên có thể hỏi
- `expected_answer` phải là câu trả lời AI TA tốt cần đưa ra
- **Không** cần fill `expected_retrieval_ids` (để `[]` là được)
- Nếu không chắc format đúng chưa, chạy lại lệnh kiểm tra ở Bước 3

---

*File này được tạo bởi Coding Agent cho Nghĩa — Lab 14 AI Evaluation Factory*
