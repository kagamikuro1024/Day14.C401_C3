"""
Tool: search_course_materials
Tìm kiếm tài liệu trong knowledge base khóa học.
"""

from langchain_core.tools import tool

from rag.retriever import search_documents, format_search_results


@tool
def search_course_materials(query: str) -> str:
    """Tìm kiếm thông tin trong tài liệu khóa học (slides bài giảng, code mẫu, FAQ).

    Sử dụng tool này khi cần:
    - Giải thích khái niệm lập trình C/C++ (biến, con trỏ, mảng, hàm,...)
    - Tìm ví dụ code minh họa
    - Trả lời câu hỏi về nội dung bài học
    - Tìm hướng dẫn cài đặt môi trường
    - Tra cứu FAQ (câu hỏi thường gặp)

    Args:
        query: Câu hỏi hoặc chủ đề cần tìm, viết chi tiết để kết quả chính xác.
               Ví dụ: "cách khai báo con trỏ trong C", "vòng lặp for ví dụ",
               "lỗi segmentation fault là gì"
    """
    try:
        results = search_documents(query, k=5)
        if not results:
            return "Không tìm thấy tài liệu liên quan trong knowledge base khóa học."

        formatted = format_search_results(results)
        return f"Kết quả tìm kiếm từ tài liệu khóa học:\n\n{formatted}"

    except FileNotFoundError:
        return ("⚠️ FAISS index chưa được build. "
                "Chạy 'python -m rag.indexer' trước khi sử dụng.")
    except Exception as e:
        return f"Lỗi khi tìm kiếm: {str(e)}"
