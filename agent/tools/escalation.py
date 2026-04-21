"""
Tool: escalate_to_human_ta
Leo thang câu hỏi cho TA người thật.
"""

from datetime import datetime
from langchain_core.tools import tool


@tool
def escalate_to_human_ta(
    student_question: str,
    summary: str,
    reason: str,
    attempted_solutions: str = "",
) -> str:
    """Leo thang câu hỏi phức tạp cho Trợ giảng (TA) người thật xử lý.

    CHỈ sử dụng tool này khi:
    - Câu hỏi quá phức tạp, vượt ngoài nội dung khóa học cơ bản
    - Lỗi liên quan đến cấu hình hệ thống/môi trường đặc thù mà AI không giải quyết được
    - Học viên yêu cầu nói chuyện trực tiếp với TA người thật
    - Vấn đề cần quyền hạn đặc biệt (gia hạn deadline, xin điểm,...)
    - AI đã thử hỗ trợ nhưng không giải quyết được sau nhiều lần

    KHÔNG dùng tool này cho:
    - Câu hỏi kiến thức cơ bản (dùng search_course_materials)
    - Debug code thông thường (dùng analyze_code_error)
    - Hỏi thông tin khóa học (dùng get_course_info)

    Args:
        student_question: Câu hỏi gốc của học viên (copy nguyên văn)
        summary: Tóm tắt ngắn gọn vấn đề (1-2 câu)
        reason: Lý do cần escalate cho TA người thật
        attempted_solutions: Những gì AI đã thử hỗ trợ trước khi escalate
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    tag_level = "🚨 HIGH" if "policy" in reason.lower() or "trực tiếp" in reason.lower() else "⚠️ MEDIUM"
    
    report = f"""
╔══════════════════════════════════════════════════════╗
║         🚨 ESCALATION REPORT — CẦN TA HỖ TRỢ        ║
╠══════════════════════════════════════════════════════╣
║ Thời gian: {timestamp}
║ Mức độ: ⚠️ Cần TA người thật
╠══════════════════════════════════════════════════════╣

📝 TÓM TẮT DÀNH CHO TA:
[Mức độ: {tag_level}] - [{summary}] - [{attempted_solutions if attempted_solutions else "Chưa thử hỗ trợ cụ thể"}]

❓ CÂU HỎI GỐC CỦA HỌC VIÊN:
{student_question}

🔍 LÝ DO ESCALATE:
{reason}

╠══════════════════════════════════════════════════════╣
║ 📧 TA chính: Trần Thị Hoa — hoa.tt@university.edu.vn
║ 📧 TA phụ: Lê Minh Tuấn — tuan.lm@university.edu.vn
║ ⏰ TA available: T2-T6 18:00-21:00 | T7 9:00-12:00
╚══════════════════════════════════════════════════════╝
"""

    response = (
        f"Mình đã chuẩn bị Phiếu yêu cầu hỗ trợ (Escalation Report) bên dưới. Bạn vui lòng kiểm tra và bấm xác nhận để gửi cho TA nhé!\n\n"
        f"--- ESCALATION REPORT ---\n{report}"
    )

    return response
