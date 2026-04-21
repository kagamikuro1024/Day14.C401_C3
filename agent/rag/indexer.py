"""
RAG Indexer — Nạp tài liệu vào FAISS vector store.

Chạy: python -m rag.indexer
"""

import os
import glob
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_core.documents import Document

import config


def load_markdown_files(directory: Path) -> list[Document]:
    """Load tất cả file .md từ thư mục, giữ metadata."""
    documents = []
    for filepath in sorted(directory.glob("*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Xác định source type từ đường dẫn
        if "slides" in str(filepath):
            source_type = "slide"
        elif "faq" in str(filepath).lower():
            source_type = "faq"
        else:
            source_type = "document"

        doc = Document(
            page_content=content,
            metadata={
                "source": filepath.name,
                "source_type": source_type,
                "full_path": str(filepath),
            }
        )
        documents.append(doc)
        print(f"  ✅ Loaded: {filepath.name} ({len(content)} chars)")

    return documents


def load_code_samples(directory: Path) -> list[Document]:
    """Load tất cả file code mẫu (.c, .cpp)."""
    documents = []
    for ext in ["*.c", "*.cpp"]:
        for filepath in sorted(directory.glob(ext)):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            doc = Document(
                page_content=content,
                metadata={
                    "source": filepath.name,
                    "source_type": "code_sample",
                    "language": "c" if filepath.suffix == ".c" else "cpp",
                    "full_path": str(filepath),
                }
            )
            documents.append(doc)
            print(f"  ✅ Loaded: {filepath.name} ({len(content)} chars)")

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """Chia nhỏ tài liệu thành chunks."""
    # Markdown Header Splitter — chia theo heading
    md_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "chapter"),
            ("##", "section"),
            ("###", "subsection"),
        ],
        strip_headers=False,
    )

    # Recursive Character Splitter — chia nhỏ hơn nếu chunk quá dài
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    all_chunks = []

    for doc in documents:
        if doc.metadata.get("source_type") == "code_sample":
            # Code samples — giữ nguyên hoặc chia nhỏ bằng text splitter
            chunks = text_splitter.split_documents([doc])
        else:
            # Markdown — chia theo heading trước, rồi chia nhỏ
            md_chunks = md_splitter.split_text(doc.page_content)
            # Thêm metadata gốc vào mỗi chunk
            for chunk in md_chunks:
                chunk.metadata.update(doc.metadata)
            # Chia nhỏ hơn nếu cần
            chunks = text_splitter.split_documents(md_chunks)

        all_chunks.extend(chunks)

    return all_chunks


def build_index():
    """Build FAISS index từ toàn bộ knowledge base."""
    print("🔨 Building FAISS index...\n")

    # 1. Load tài liệu
    print("📂 Loading slides...")
    slide_docs = load_markdown_files(config.SLIDES_DIR)

    print("\n📂 Loading FAQ...")
    faq_docs = load_markdown_files(config.KNOWLEDGE_BASE_DIR)
    # Lọc chỉ lấy faq.md
    faq_docs = [d for d in faq_docs if "faq" in d.metadata["source"].lower()]

    print("\n📂 Loading code samples...")
    code_docs = load_code_samples(config.CODE_SAMPLES_DIR)

    all_docs = slide_docs + faq_docs + code_docs
    print(f"\n📄 Tổng cộng: {len(all_docs)} tài liệu")

    # 2. Chia nhỏ
    print("\n✂️  Splitting documents...")
    chunks = split_documents(all_docs)
    print(f"📦 Tổng chunks: {len(chunks)}")

    # 3. Tạo embeddings và FAISS index
    print("\n🧠 Creating embeddings & FAISS index...")
    embeddings = OpenAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        openai_api_key=config.OPENAI_API_KEY,
    )

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    # 4. Lưu index
    config.FAISS_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(config.FAISS_INDEX_DIR))
    print(f"\n💾 Index saved to: {config.FAISS_INDEX_DIR}")
    print(f"✅ Done! {len(chunks)} chunks indexed.")

    return vector_store


if __name__ == "__main__":
    build_index()
