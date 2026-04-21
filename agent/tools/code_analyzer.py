"""
Tool: analyze_code_error
Phân tích lỗi code C/C++ của học viên.
"""

from langchain_core.tools import tool

from rag.retriever import search_documents, format_search_results


@tool
def analyze_code_error(code: str, error_description: str) -> str:
    """Phân tích lỗi trong code C/C++ và gợi ý cách sửa.

    Sử dụng tool này khi học viên:
    - Gửi đoạn code bị lỗi cần debug
    - Gặp lỗi biên dịch (compilation error)
    - Gặp lỗi runtime (segmentation fault, infinite loop,...)
    - Code chạy nhưng kết quả sai (logic error)
    - Cần review code

    Args:
        code: Đoạn code C/C++ của học viên (copy nguyên văn code)
        error_description: Mô tả lỗi gặp phải, bao gồm thông báo lỗi
                          từ compiler nếu có. Ví dụ: "lỗi segmentation fault khi chạy",
                          "compiler báo expected ; before", "kết quả ra 0 thay vì 3.5"
    """
    # Tìm tài liệu liên quan để hỗ trợ phân tích
    search_query = f"lỗi C/C++ {error_description}"
    related_docs = search_documents(search_query, k=3)
    related_info = format_search_results(related_docs) if related_docs else ""

    analysis = f"""## Phân tích code của học viên

### Code nhận được:
```c
{code}
```

### Lỗi được mô tả:
{error_description}

### Tài liệu tham khảo từ khóa học:
{related_info}

---
Dựa vào code, mô tả lỗi, và tài liệu khóa học,
hãy phân tích nguyên nhân lỗi và gợi ý cách sửa theo phương pháp sư phạm
(gợi ý hướng đi, không đưa đáp án trực tiếp trừ khi học viên thật sự bế tắc).
"""
    return analysis
