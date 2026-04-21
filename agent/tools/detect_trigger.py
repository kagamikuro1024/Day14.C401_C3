"""
Tool: detect_escalation_trigger
Phát hiện khi cần escalate câu hỏi lên TA người thật.

Các trigger:
1. Trigger 1: Sinh viên chủ động yêu cầu (request)
2. Trigger 2: Thông tin đã tra cứu nhưng không tìm được (missing_info)
3. Trigger 3: Sinh viên phản bác lại câu trả lời (dispute)
"""

from langchain_core.tools import tool
import re


@tool
def detect_escalation_trigger(
    user_message: str,
    attempt_count: int = 0,
    ai_response_previous: str = ""
) -> dict:
    """Phát hiện xem sinh viên có yêu cầu gọi TA hay không.
    
    Args:
        user_message: Tin nhắn của sinh viên
        attempt_count: Số lần AI đã thử trả lời (mặc định 0)
        ai_response_previous: Câu trả lời trước đó của AI (nếu có)
    
    Returns:
        {
            "should_escalate": bool,
            "trigger_type": str ("direct_request" | "missing_info" | "dispute" | None),
            "confidence": float (0-1),
            "reason": str,
            "action": str (gợi ý action tiếp theo)
        }
    """
    
    message_lower = user_message.lower()
    
    # === TRIGGER 1: DIRECT REQUEST ===
    # Từ khóa chỉ ra sinh viên muốn chuyển cho TA
    direct_request_keywords = [
        r"(gọi|chuyển|tag|@).{0,5}(ta|giảng viên|trợ giảng|teacher|instructor)",
        r"(hỏi|gửi|liên hệ).{0,5}(ta|TA|trợ giảng)",
        r"^(ta|TA|trợ giảng)[\s,]",
        r"(cần|muốn).{0,5}(nói|chuyện|hỏi).{0,5}(ta|trợ giảng)",
        r"(xin|tìm).{0,5}(sự giúp đỡ|trợ giúp).{0,5}(của.{0,5})?(ta|trợ giảng)",
        r"^(mê|ay|help|sos)[\s,]",  # SOS signals
        r"(policy|quy chế|xin phép|điểm thi|phúc khảo|khiếu nại|ngoại lệ)", # Force escalate policy issues
    ]
    
    for pattern in direct_request_keywords:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return {
                "should_escalate": True,
                "trigger_type": "direct_request",
                "confidence": 0.95,
                "reason": "Sinh viên chủ động yêu cầu chuyên cho TA/Giảng viên",
                "action": "🚀 Kích hoạt Route TA ngay lập tức. Không thải lại toàn bộ câu hỏi."
            }
    
    # === TRIGGER 2: DISPUTE (Phản bác) ===
    dispute_keywords = [
        r"(sai|không đúng|bạn trả lời sai|bot bị lỗi)",
        r"(không phải vậy|không phải cái|ý mình khác)",
        r"(bạn không hiểu|hiểu sai ý mình)",
        r"(mình không hiểu|chưa rõ|vẫn không biết)",
    ]
    
    for pattern in dispute_keywords:
        if re.search(pattern, message_lower, re.IGNORECASE):
            return {
                "should_escalate": False, # KHÔNG gọi escalate ngay, yêu cầu AI hỏi trước
                "trigger_type": "dispute",
                "confidence": 0.80,
                "reason": "Sinh viên phản bác lại câu trả lời",
                "action": "🚨 KHOAN Escalate: Sinh viên không hài lòng. HÃY HỎI sinh viên: 'Bạn có muốn chuyển câu hỏi này cho TA/Giảng viên để kiểm tra chính xác không?'"
            }
    
    # === No Trigger ===
    return {
        "should_escalate": False,
        "trigger_type": None,
        "confidence": 0.0,
        "reason": "Không phát hiện trigger escalation",
        "action": "Tiếp tục hỗ trợ bình thường"
    }
