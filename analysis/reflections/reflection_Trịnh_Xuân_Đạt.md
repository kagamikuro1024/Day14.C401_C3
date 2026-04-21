## Họ tên: Trịnh Xuân Đạt
## Mã số sinh viên: 2A202600326
## Lớp: C401-C3
## Reflection: Synthetic Data Generation for LLM Evaluation

## Những gì đã làm
- Implement data/synthetic_gen.py với real GPT-4o API call
- Tạo 50+ test cases từ knowledge_base khóa học
- Hỗ trợ async/concurrent generation
- Phân bố: factual/debug/adversarial theo tỉ lệ 60/20/20

## Kết quả
- Tạo ra 56 cases trong data/golden_set.jsonl
- Chạy trong 13 giây