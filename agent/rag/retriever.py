"""
RAG Retriever — Load FAISS index và thực hiện similarity search.
"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

import config


_vector_store = None  # Singleton cache


def load_vector_store() -> FAISS:
    """Load FAISS vector store từ disk (singleton)."""
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    if not config.FAISS_INDEX_DIR.exists():
        raise FileNotFoundError(
            f"FAISS index not found at {config.FAISS_INDEX_DIR}. "
            f"Run 'python -m rag.indexer' first."
        )

    embeddings = OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY,
    )

    _vector_store = FAISS.load_local(
        str(config.FAISS_INDEX_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return _vector_store


def search_documents(
    query: str,
    k: int = config.RETRIEVAL_K,
    source_type: str = None,
    score_threshold: float = None,
) -> list[Document]:
    """
    Tìm tài liệu liên quan nhất trong knowledge base.

    Cải tiến so với phiên bản cũ:
    - Thêm score_threshold để lọc kết quả có similarity quá thấp
    - FAISS dùng L2 distance: giá trị nhỏ hơn = tốt hơn
    - Khi score_threshold=None: trả về top-k như bình thường (backward-compatible)

    Args:
        query: Câu hỏi cần tìm
        k: Số lượng tài liệu trả về
        source_type: Lọc theo loại (slide, faq, code_sample)
        score_threshold: Ngưỡng L2 distance tối đa (None = không lọc)
                         Dưới 0.3: rất gần, Dưới 0.5: liên quan, Trên 0.8: ít liên quan

    Returns:
        Danh sách Document với nội dung liên quan
    """
    store = load_vector_store()

    # Lấy nhiều hơn nếu có filter (để bù sau khi lọc)
    fetch_k = k * 3 if (source_type or score_threshold) else k

    results_with_scores = store.similarity_search_with_score(query, k=fetch_k)

    # Lọc theo source_type nếu có
    if source_type:
        results_with_scores = [
            (doc, score) for doc, score in results_with_scores
            if doc.metadata.get("source_type") == source_type
        ]

    # Lọc theo score threshold nếu có (L2 distance nhỏ = tốt hơn)
    if score_threshold is not None:
        results_with_scores = [
            (doc, score) for doc, score in results_with_scores
            if score <= score_threshold
        ]

    # Sắp xếp theo score tăng dần (nhỏ hơn = tốt hơn) và giới hạn k kết quả
    results_with_scores.sort(key=lambda x: x[1])
    return [doc for doc, _ in results_with_scores[:k]]


def search_with_scores(
    query: str,
    k: int = config.RETRIEVAL_K,
) -> list[tuple[Document, float]]:
    """Tìm tài liệu kèm điểm similarity."""
    store = load_vector_store()
    return store.similarity_search_with_score(query, k=k)


def format_search_results(documents: list[Document]) -> str:
    """Format kết quả tìm kiếm thành text đẹp."""
    if not documents:
        return "Không tìm thấy tài liệu liên quan."

    formatted = []
    for i, doc in enumerate(documents, 1):
        source = doc.metadata.get("source", "N/A")
        source_type = doc.metadata.get("source_type", "N/A")
        section = doc.metadata.get("section", "")
        subsection = doc.metadata.get("subsection", "")

        header = f"📄 Nguồn {i}: {source}"
        if section:
            header += f" > {section}"
        if subsection:
            header += f" > {subsection}"
        header += f" [{source_type}]"

        formatted.append(f"{header}\n{doc.page_content}")

    return "\n\n---\n\n".join(formatted)
