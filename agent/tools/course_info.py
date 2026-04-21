"""
Tool: get_course_info
Tra cứu thông tin khóa học.
"""

import json
from langchain_core.tools import tool

import config


def _load_course_info() -> dict:
    """Load thông tin khóa học từ JSON."""
    with open(config.COURSE_INFO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@tool
def get_course_info(info_type: str) -> str:
    """Tra cứu thông tin về khóa học Lập trình C/C++ cơ bản.

    Sử dụng tool này khi học viên hỏi về:
    - Lịch học, phòng học
    - Thông tin giảng viên, TA
    - Cách tính điểm, trọng số
    - Lịch thi, deadline
    - Tài liệu tham khảo, sách giáo khoa
    - Link tài nguyên học tập
    - Quy chế khóa học (vắng, nộp trễ, đạo văn)
    - Syllabus (chương trình học theo tuần)

    Args:
        info_type: Loại thông tin cần tra cứu. Có thể là một trong:
                   - "schedule" (lịch học)
                   - "instructor" (giảng viên)
                   - "ta" (trợ giảng)
                   - "grading" (cách tính điểm)
                   - "syllabus" (chương trình học)
                   - "resources" (tài liệu, link)
                   - "policies" (quy chế)
                   - "dates" (ngày quan trọng, deadline cụ thể của lab, project, bài tập)
                   - "all" (tất cả thông tin)
    """
    try:
        info = _load_course_info()
    except Exception as e:
        return f"Lỗi đọc file thông tin khóa học: {str(e)}"

    info_type = info_type.lower().strip()

    if info_type in ("schedule", "lịch học", "lich hoc"):
        theory = info["schedule"]["theory"]
        lab = info["schedule"]["lab"]
        return (
            f"📅 LỊCH HỌC — {info['course_name']} ({info['semester']})\n\n"
            f"🏫 Lý thuyết:\n"
            f"  • Ngày: {theory['day']}\n"
            f"  • Thời gian: {theory['time']}\n"
            f"  • Phòng: {theory['room']}\n"
            f"  • Ghi chú: {theory['note']}\n\n"
            f"💻 Thực hành:\n"
            f"  • Ngày: {lab['day']}\n"
            f"  • Thời gian: {lab['time']}\n"
            f"  • Phòng: {lab['room']}\n"
            f"  • Ghi chú: {lab['note']}"
        )

    elif info_type in ("instructor", "giảng viên", "giang vien", "gv"):
        inst = info["instructor"]
        return (
            f"👨‍🏫 GIẢNG VIÊN\n\n"
            f"  • Tên: {inst['name']}\n"
            f"  • Email: {inst['email']}\n"
            f"  • Office hours: {inst['office_hours']}\n"
            f"  • Văn phòng: {inst['office']}"
        )

    elif info_type in ("ta", "trợ giảng", "tro giang"):
        tas = info["teaching_assistants"]
        result = "👩‍💼 DANH SÁCH TRỢ GIẢNG\n\n"
        for ta in tas:
            result += (
                f"  • {ta['name']} ({ta['role']})\n"
                f"    Email: {ta['email']}\n"
                f"    Available: {ta['available']}\n\n"
            )
        return result.strip()

    elif info_type in ("grading", "điểm", "diem", "cách tính điểm", "trừ điểm"):
        info_full = _load_course_info()
        
        # Try new format first (components + assessment_types)
        if "components" in info_full.get("grading", {}):
            grading = info_full["grading"]
            result = "📊 CÁCH TÍNH ĐIỂM CHI TIẾT\n\n"
            
            # Components
            result += "**1️⃣ Các thành phần điểm:**\n"
            for key, val in grading["components"].items():
                result += f"  • {val['description']}: {val['weight']}%\n"
            
            # Note
            if "note" in grading:
                result += f"\n**📝 Ghi chú:** {grading['note']}\n"
            
            # Assessment types
            if "assessment_types" in info_full:
                result += "\n**2️⃣ Chi tiết các loại bài tập:**\n"
                assess = info_full["assessment_types"]
                
                if "weekly_assignments" in assess:
                    wa = assess["weekly_assignments"]
                    result += f"\n🔹 **Bài tập hàng tuần:**\n"
                    result += f"   • Tần suất: {wa.get('frequency', 'N/A')}\n"
                    result += f"   • Nộp: {wa.get('submission', 'N/A')}\n"
                    result += f"   • Deadline policy: {wa.get('deadline_policy', 'N/A')}\n"
                
                if "labs" in assess:
                    lab = assess["labs"]
                    result += f"\n🔹 **Bài tập Lab:**\n"
                    result += f"   • Tần suất: {lab.get('frequency', 'N/A')}\n"
                    result += f"   • Deadline policy: {lab.get('deadline_policy', 'N/A')}\n"
                
                if "projects" in assess:
                    proj = assess["projects"]
                    result += f"\n🔹 **Project ({proj.get('count', 'N/A')} dự án):**\n"
                    result += f"   • Deadline policy: {proj.get('deadline_policy', 'N/A')}\n"
                    for p_key in ["project_1", "project_2", "project_3"]:
                        if p_key in proj:
                            p = proj[p_key]
                            result += f"   • {p['title']}: {p['deadline']}\n"
            
            return result.strip()
        else:
            # Fallback to old format
            grades = info_full.get("grading", {})
            result = "📊 CÁCH TÍNH ĐIỂM\n\n"
            for key, val in grades.items():
                if isinstance(val, dict) and 'description' in val:
                    result += f"  • {val['description']}: {val.get('weight', 'N/A')}%\n"
            return result.strip()

    elif info_type in ("syllabus", "chương trình", "chuong trinh"):
        syllabus = info["syllabus"]
        result = "📖 CHƯƠNG TRÌNH HỌC THEO TUẦN\n\n"
        for week in syllabus:
            result += f"  Tuần {week['week']:2d}: {week['topic']} (Chương {week['chapter']})\n"
        return result.strip()

    elif info_type in ("resources", "tài liệu", "tai lieu", "link"):
        res = info["resources"]
        result = f"📚 TÀI LIỆU THAM KHẢO\n\n"
        result += f"📕 Sách giáo khoa: {res['textbook']}\n\n"
        result += "📗 Sách tham khảo:\n"
        for book in res["references"]:
            result += f"  • {book}\n"
        result += "\n🌐 Tài nguyên online:\n"
        for link in res["online"]:
            result += f"  • {link['name']}: {link['url']}\n"
        result += "\n🛠️ Công cụ:\n"
        for tool_info in res["tools"]:
            result += f"  • {tool_info['name']}: {tool_info['url']} ({tool_info['note']})\n"
        result += f"\n🖥️ LMS: {res['lms']}"
        return result

    elif info_type in ("policies", "quy chế", "quy che", "nội quy", "vắng", "vắng mặt", "absence"):
        pol = info["policies"]
        return (
            f"📋 QUY CHẾ KHÓA HỌC\n\n"
            f"  • Nộp trễ: {pol['late_submission']}\n"
            f"  • Đạo văn: {pol['plagiarism']}\n"
            f"  • Vắng mặt: {pol['absence']}\n"
            f"  • Liên lạc: {pol['communication']}"
        )

    elif info_type in ("dates", "ngày quan trọng", "ngay quan trong", "deadline"):
        dates = info["important_dates"]
        result = (
            f"📆 CÁC NGÀY QUAN TRỌNG\n\n"
            f"  • Bắt đầu: {dates['start']}\n"
            f"  • Kiểm tra giữa kỳ: {dates['midterm']}\n"
            f"  • Deadline project chung: {dates['project_deadline']}\n"
            f"  • Thi cuối kỳ: {dates['final_exam']}\n"
            f"  • Kết thúc: {dates['end']}\n"
        )
        
        if "assessment_types" in info:
            result += "\n⏳ CHI TIẾT DEADLINE & NỘP TRỄ:\n"
            assess = info["assessment_types"]
            
            if "projects" in assess:
                proj = assess["projects"]
                result += f"\n🔹 **Projects:**\n"
                for p_key in ["project_1", "project_2", "project_3"]:
                    if p_key in proj:
                        result += f"   • {proj[p_key]['title']}: {proj[p_key]['deadline']}\n"
                result += f"   • Policy Nộp trễ: {proj.get('deadline_policy', 'N/A')}\n"
                
            if "weekly_assignments" in assess:
                wa = assess["weekly_assignments"]
                result += f"\n🔹 **Weekly Assignments:**\n"
                result += f"   • Nộp: {wa.get('submission', 'N/A')}\n"
                result += f"   • Policy Nộp trễ: {wa.get('deadline_policy', 'N/A')}\n"
                
            if "labs" in assess:
                lab = assess["labs"]
                result += f"\n🔹 **Labs:**\n"
                result += f"   • Nộp: {lab.get('submission', 'N/A')}\n"
                result += f"   • Policy Nộp trễ: {lab.get('deadline_policy', 'N/A')}\n"
                
        return result

    elif info_type == "all":
        return json.dumps(info, ensure_ascii=False, indent=2)

    else:
        return (
            f"Không nhận ra loại thông tin '{info_type}'. "
            f"Các loại hỗ trợ: schedule, instructor, ta, grading, "
            f"syllabus, resources, policies, dates, all"
        )
