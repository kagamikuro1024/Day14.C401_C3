# 📋 Kế Hoạch Cá Nhân — Đạt

> **Vai trò:** Contributor — Phát triển Synthetic Data Generator (SDG)
> **Nhánh Git:** `feature/dat-sdg-engine`
> **Độ khó task:** ⭐⭐ Trung bình

---

## 🎯 Nhiệm Vụ Của Đạt

Đạt chịu trách nhiệm **implement script tự động sinh test cases** (`data/synthetic_gen.py`) sử dụng OpenAI API để tạo ≥ 50 test cases chất lượng cao từ tài liệu khóa học. Script cần hoạt động **async** để chạy song song nhanh hơn.

**Mục tiêu cụ thể:**
- Script gọi GPT-4o thực (không dùng placeholder)
- Tạo ≥ 50 test cases từ tài liệu knowledge_base
- Có adversarial cases (câu hỏi lừa / edge case)
- Output đúng format `data/golden_set.jsonl`

---

## 📁 File Cần Sửa/Tạo

- **Sửa:** `data/synthetic_gen.py` (implement thực thay placeholder)

---

## 🌿 Bước 1: Tạo nhánh Git

```powershell
cd d:\gitHub\AI_20k\Day14\Lab14-AI-Evaluation-Benchmarking

git checkout main
git pull origin main

# Tạo nhánh của Đạt
git checkout -b feature/dat-sdg-engine

# Xác nhận
git branch
```

---

## 🔑 Bước 2: Hiểu cấu trúc dữ liệu cần tạo

Mỗi test case trong `golden_set.jsonl` cần có format sau:

```json
{
  "question": "Câu hỏi của học viên",
  "expected_answer": "Câu trả lời kỳ vọng từ AI TA",
  "context": "Đoạn tài liệu liên quan",
  "difficulty": "easy|medium|hard",
  "type": "factual|debug|adversarial",
  "expected_retrieval_ids": []
}
```

---

## 💻 Bước 3: Implement `data/synthetic_gen.py`

Thay toàn bộ nội dung file bằng code sau:

```python
"""
Synthetic Data Generator — Tự động tạo Golden Dataset từ knowledge base.
Sử dụng GPT-4o để sinh test cases đa dạng cho benchmark TA_Chatbot.
"""
import json
import asyncio
import os
from typing import List, Dict
from pathlib import Path
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Nạp API key từ .env
load_dotenv()


# Prompt template cho GPT-4o
GENERATION_PROMPT = """Bạn là chuyên gia thiết kế bài kiểm tra AI Teaching Assistant cho khóa học Lập trình C/C++ cơ bản (CS101).

Dựa vào TÀI LIỆU bên dưới, hãy tạo ĐÚNG {num_pairs} bộ câu hỏi-đáp theo TỶ LỆ sau:
- 60% câu hỏi factual: deadline, grading, khái niệm C/C++
- 20% câu hỏi debug: lỗi code, cú pháp, runtime error
- 20% câu hỏi adversarial: ngoài phạm vi, câu lừa, thông tin mơ hồ

TÀI LIỆU NGUỒN:
---
{text}
---

Trả về JSON object có key "cases" chứa array (KHÔNG kèm markdown ```):
{{
  "cases": [
    {{
      "question": "câu hỏi thực tế mà học viên hỏi",
      "expected_answer": "câu trả lời hoàn chỉnh kỳ vọng từ AI TA",
      "context": "đoạn trích liên quan từ tài liệu (< 200 ký tự)",
      "difficulty": "easy|medium|hard",
      "type": "factual|debug|adversarial",
      "expected_retrieval_ids": []
    }}
  ]
}}"""


async def generate_qa_from_text(
    text: str,
    num_pairs: int = 5,
    doc_name: str = "unknown"
) -> List[Dict]:
    """
    Tạo QA pairs từ text bằng GPT-4o.
    
    Args:
        text: Nội dung tài liệu nguồn
        num_pairs: Số cặp QA cần tạo
        doc_name: Tên tài liệu (để log)
    
    Returns:
        Danh sách dict test cases
    """
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Giới hạn text để tránh vượt context window
    text_truncated = text[:4000] if len(text) > 4000 else text
    
    prompt = GENERATION_PROMPT.format(
        num_pairs=num_pairs,
        text=text_truncated,
    )
    
    print(f"  ⚙️  Đang tạo {num_pairs} cases từ: {doc_name}...")
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,  # Đủ sáng tạo nhưng không quá ngẫu nhiên
        )
        
        content = response.choices[0].message.content
        parsed = json.loads(content)
        
        # Lấy array "cases" từ response
        cases = parsed.get("cases", [])
        if not cases and isinstance(parsed, list):
            cases = parsed
        
        print(f"  ✅ {doc_name}: tạo được {len(cases)} cases")
        return cases
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Lỗi JSON từ {doc_name}: {e}")
        return []
    except Exception as e:
        print(f"  ❌ Lỗi API cho {doc_name}: {e}")
        return []


async def main():
    """
    Hàm chính — đọc toàn bộ knowledge base và tạo golden dataset.
    """
    load_dotenv()
    
    # Đường dẫn đến knowledge base
    kb_dir = Path("agent/knowledge_base")
    
    if not kb_dir.exists():
        print(f"❌ Không tìm thấy thư mục: {kb_dir}")
        return
    
    # Thu thập tất cả tài liệu
    doc_sources = []
    
    # Đọc slides (các file .md trong slides/)
    slides_dir = kb_dir / "slides"
    if slides_dir.exists():
        for md_file in sorted(slides_dir.glob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            doc_sources.append((content, md_file.name))
            
    # Đọc FAQ
    faq_path = kb_dir / "faq.md"
    if faq_path.exists():
        content = faq_path.read_text(encoding="utf-8")
        doc_sources.append((content, "faq.md"))
    
    if not doc_sources:
        print("❌ Không tìm thấy tài liệu trong knowledge_base!")
        return
    
    print(f"📚 Tìm thấy {len(doc_sources)} tài liệu nguồn")
    print(f"🚀 Bắt đầu tạo test cases (chạy song song)...\n")
    
    # Tính số cases cần tạo cho mỗi tài liệu (đảm bảo tổng >= 50)
    target_total = 55  # Tạo thêm 5 để backup
    pairs_per_doc = max(5, target_total // len(doc_sources) + 1)
    
    # Tạo tasks song song cho tất cả tài liệu
    tasks = [
        generate_qa_from_text(text, num_pairs=pairs_per_doc, doc_name=name)
        for text, name in doc_sources
    ]
    
    # Chạy song song tất cả
    all_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Gộp tất cả cases
    all_cases = []
    for result in all_results:
        if isinstance(result, list):
            all_cases.extend(result)
        elif isinstance(result, Exception):
            print(f"⚠️ Lỗi task: {result}")
    
    # Đảm bảo đủ 50 cases
    if len(all_cases) < 50:
        print(f"\n⚠️ Mới có {len(all_cases)} cases, cần thêm...")
        # Tạo thêm từ tài liệu đầu tiên
        extra = await generate_qa_from_text(
            doc_sources[0][0], 
            num_pairs=50 - len(all_cases) + 5,
            doc_name="extra_generation"
        )
        all_cases.extend(extra)
    
    print(f"\n📊 Tổng cases tạo được: {len(all_cases)}")
    
    # Lưu vào file JSONL
    os.makedirs("data", exist_ok=True)
    output_path = "data/golden_set.jsonl"
    
    with open(output_path, "w", encoding="utf-8") as f:
        for case in all_cases:
            # Đảm bảo có đủ trường
            case.setdefault("expected_retrieval_ids", [])
            case.setdefault("difficulty", "medium")
            case.setdefault("type", "factual")
            f.write(json.dumps(case, ensure_ascii=False) + "\n")
    
    print(f"✅ Done! {len(all_cases)} cases → {output_path}")
    
    # Thống kê phân bố
    types = {}
    difficulties = {}
    for c in all_cases:
        t = c.get("type", "unknown")
        d = c.get("difficulty", "unknown")
        types[t] = types.get(t, 0) + 1
        difficulties[d] = difficulties.get(d, 0) + 1
    
    print(f"\n📈 Phân bố theo loại: {types}")
    print(f"📈 Phân bố theo độ khó: {difficulties}")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧪 Bước 4: Kiểm tra script

```powershell
# Kiểm tra cơ bản (không gọi API — chỉ import)
python -c "
import ast
with open('data/synthetic_gen.py') as f:
    ast.parse(f.read())
print('✅ Syntax OK')
"

# Chạy thực (gọi API — mất khoảng 2-5 phút)
python data/synthetic_gen.py
```

**Output kỳ vọng:**
```
📚 Tìm thấy N tài liệu nguồn
🚀 Bắt đầu tạo test cases (chạy song song)...
  ⚙️ Đang tạo X cases từ: chapter01.md...
  ✅ chapter01.md: tạo được X cases
  ...
✅ Done! 50+ cases → data/golden_set.jsonl
📈 Phân bố theo loại: {'factual': N, 'debug': N, 'adversarial': N}
```

```powershell
# Kiểm tra kết quả
python -c "
import json
with open('data/golden_set.jsonl') as f:
    cases = [json.loads(l) for l in f if l.strip()]
print(f'Total: {len(cases)} cases')
assert len(cases) >= 50, f'Cần ít nhất 50 cases! Mới có: {len(cases)}'
print('✅ Đủ 50+ cases!')
"
```

---

## 💾 Bước 5: Commit

```powershell
git add data/synthetic_gen.py
git add data/golden_set.jsonl  # Nếu đã chạy thành công

git commit -m "feat: implement SDG script gọi GPT-4o thực

- Thay toàn bộ placeholder bằng async OpenAI API call
- Tạo 50+ test cases từ knowledge_base khóa học CS101
- Có phân bố: factual (60%), debug(20%), adversarial (20%)
- Chạy song song bằng asyncio.gather"

git push origin feature/dat-sdg-engine
```

---

## 🔗 Bước 6: Tạo Pull Request

1. Vào GitHub repo
2. Click **"Compare & pull request"**
3. Điền:
   - **Title:** `[Đạt] feat: SDG script tạo 50+ golden test cases từ GPT-4o`
   - **Description:**
     ```
     ## Những gì đã làm
     - Implement data/synthetic_gen.py với real GPT-4o API call
     - Tạo 50+ test cases từ knowledge_base khóa học
     - Hỗ trợ async/concurrent generation
     - Phân bố: factual/debug/adversarial

     ## Kết quả
     - X cases trong data/golden_set.jsonl
     - Chạy trong X giây

     ## Cách kiểm tra
     python data/synthetic_gen.py
     ```
4. **Reviewer: Trung**
5. Click **"Create Pull Request"**

---

## ⚠️ Lưu Ý

- Script chạy có tốn **API credits** — chỉ chạy khi cần thiết
- Nếu lỗi `AuthenticationError` → kiểm tra `OPENAI_API_KEY` trong file `.env`
- Nếu lỗi `RateLimitError` → giảm `pairs_per_doc` xuống hoặc thêm `await asyncio.sleep(2)` giữa batch
- **Không commit** file `.env` lên Git!

---

*File này được tạo bởi Coding Agent cho Đạt — Lab 14 AI Evaluation Factory*
