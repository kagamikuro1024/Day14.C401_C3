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
) -> list[Document]:
    """
    Tìm tài liệu liên quan nhất trong knowledge base.

    Args:
        query: Câu hỏi cần tìm
        k: Số lượng tài liệu trả về
        source_type: Lọc theo loại (slide, faq, code_sample)

    Returns:
        Danh sách Document với nội dung liên quan
    """
    store = load_vector_store()

    if source_type:
        filter_dict = {"source_type": source_type}
        results = store.similarity_search(query, k=k, filter=filter_dict)
    else:
        results = store.similarity_search(query, k=k)

    return results


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
