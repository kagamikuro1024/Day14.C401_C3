## Họ tên: Trịnh Xuân Đạt
## Mã số sinh viên: 2A202600326
## Lớp: C401-C3
## Reflection: Synthetic Data Generation for LLM Evaluation


## Engineering Contribution	
### Những gì đã làm
- Implement data/synthetic_gen.py với real GPT-4o API call
- Tạo 50+ test cases từ knowledge_base khóa học
- Hỗ trợ async/concurrent generation
- Phân bố: factual/debug/adversarial theo tỉ lệ 60/20/20

### Kết quả
- Tạo ra 56 cases trong data/golden_set.jsonl
- Chạy trong 13 giây

## Technical Depth
- MRR là một metric đánh giá hiệu suất của hệ thống trả lời câu hỏi, đo lường vị trí của câu trả lời đúng trong danh sách kết quả trả về. Cohen's Kappa là một thống kê đo lường sự đồng thuận giữa hai đánh giá viên, điều chỉnh cho sự đồng thuận ngẫu nhiên. Position Bias là hiện tượng khi người dùng có xu hướng chọn các kết quả ở vị trí cao hơn trong danh sách kết quả, bất kể chất lượng của chúng.
- Chi phí liên quan đến việc sử dụng API của GPT-4o, trong khi chất lượng liên quan đến độ chính xác và tính đa dạng của các test cases được tạo ra. Trade-off giữa hai yếu tố này là một vấn đề quan trọng cần cân nhắc khi thiết kế hệ thống đánh giá.

## Problem Solving
- Để đảm bảo chất lượng của các test cases, tôi đã sử dụng một tập hợp các câu hỏi từ knowledge_base khóa học, sau đó phân loại chúng thành factual, debug và adversarial. Tôi cũng đã sử dụng async/concurrent generation để tối ưu hóa thời gian tạo test cases.
- Để giải quyết vấn đề position bias, tôi đã đảm bảo rằng các test cases được phân bố ngẫu nhiên trong danh sách kết quả, thay vì chỉ tập trung vào các vị trí cao hơn.