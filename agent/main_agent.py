"""
MainAgent — Async wrapper cho TA_Chatbot (agent.py).

Mục đích:
- Cung cấp interface async để BenchmarkRunner gọi được
- Capture retrieved_ids từ FAISS (dùng để tính Hit Rate / MRR)
- Không thay đổi logic của agent gốc
"""
import asyncio
import sys
import os

# Đảm bảo import được package agent
sys.path.insert(0, os.path.dirname(__file__))

from agent import chat
from rag.retriever import search_documents


class MainAgent:
    """
    Async wrapper của TA_Chatbot phục vụ evaluation pipeline.

    Interface chuẩn cho BenchmarkRunner:
        result = await agent.query("câu hỏi")
        result["answer"]        → chuỗi câu trả lời
        result["retrieved_ids"] → danh sách chunk_id đã retrieve
    """

    async def query(self, question: str) -> dict:
        """
        Gọi TA_Chatbot và trả về dict chuẩn cho BenchmarkRunner.

        Chạy chat() đồng bộ trong thread pool để không block event loop,
        đồng thời capture retrieved_ids từ FAISS retriever.

        Args:
            question: Câu hỏi từ học viên

        Returns:
            dict với:
                - "answer": str — câu trả lời của agent
                - "retrieved_ids": list[str] — chunk_id các tài liệu đã retrieve
        """
        # Chạy song song: chat() và search_documents() trong thread pool
        answer_task = asyncio.to_thread(chat, question)
        retrieval_task = asyncio.to_thread(search_documents, question, 6)

        answer, docs = await asyncio.gather(answer_task, retrieval_task)

        # Lấy chunk_id từ metadata của mỗi document
        retrieved_ids = [
            doc.metadata.get("chunk_id", f"no_id_{i}")
            for i, doc in enumerate(docs)
        ]

        return {
            "answer": answer,
            "retrieved_ids": retrieved_ids,
        }
