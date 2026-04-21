**Họ và tên**: Nguyễn Thành Vinh
**Mã số**: 2A202600206
**Nhóm**: C401-C3

## Đóng góp cá nhân
Triển khai các module trong file `engine/llm_judge.py`

commit:
```
feat: implement Multi-Judge Consensus System (GPT-4o + Gemini-2.5-Pro)
- Implement real async API calls cho GPT-4o và Gemini-2.5-Pro
- Chạy 2 judges song song bằng asyncio.gather
- Tính agreement rate tự động với công thức dựa trên score diff
- Phát hiện conflict khi |accuracy_diff| > 1 (tự động flag needs_human_review)
- Thêm position bias detection method (đổi thứ tự A/B)
- Xử lý lỗi API riêng cho mỗi judge (fallback score = 3)
```

## Mục tiêu đã hoàn thành
- Định nghĩa Accuracy, Completeness, Professionalism cho rubric trong `JUDGE_PROMPT`.
- Triển khai song song **GPT-4o** và **Gemini-2.5-Pro**.
- Triển khai hàm `_calculate_agreement` và `flag needs_human_review` khi `accuracy_diff > 1`.
- Triển khai logic đổi chỗ câu trả lời A/B và tính `bias_magnitude`.
- Hiểu được **Position Bias**: Thiên kiên vị trí khi mà một model được yêu câu so sánh 2 câu trả lời từ một câu hỏi. Nó sẽ hay ưu tiên câu trả lời nào xuất hiện trước trong context.
- Hiểu được **Cohen's Kappa**: là một hệ số để tính toán độ tin cậy giữa 2 chuyên gia chấm, dựa vào tỷ lệ đồng thuận quan sát được và tỷ lệ đồng thuận kỳ vọng ngẫu nhiên.

## Các cải tiến kỹ thuật đã sử dụng
- Định dạng output của 2 model dưới dạng JSON.
- Dùng `asyncio` để chạy song song 2 model.

## Một vấn đề đã giải quyết
Khi so sánh 2 model, nếu chạy tuần tự sẽ rất mất thời gian. Vì vậy, tôi đã quyết định dùng `asyncio` để chạy song song 2 model, giảm đáng kể thời gian so sánh.

