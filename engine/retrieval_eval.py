from typing import List, Dict

class RetrievalEvaluator:
    def calculate_hit_rate(self, expected_ids: List[str], retrieved_ids: List[str], top_k: int = 3) -> float:
        """
        Tính toán Hit Rate@K: xem ít nhất 1 trong expected_ids có nằm trong top_k của retrieved_ids không.
        """
        if not expected_ids or not retrieved_ids:
            return 0.0
            
        top_retrieved = retrieved_ids[:top_k]
        hit = any(doc_id in top_retrieved for doc_id in expected_ids)
        return 1.0 if hit else 0.0

    def calculate_mrr(self, expected_ids: List[str], retrieved_ids: List[str]) -> float:
        """
        Tính Mean Reciprocal Rank (MRR).
        Tìm vị trí đầu tiên của một expected_id trong retrieved_ids.
        MRR = 1 / position (vị trí 1-indexed). Nếu không thấy thì là 0.
        """
        if not expected_ids or not retrieved_ids:
            return 0.0

        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_ids:
                return 1.0 / (i + 1)
        return 0.0

    def evaluate(self, retrieved_ids: List[str], expected_ids: List[str]) -> Dict:
        """Tính toán cả Hit Rate và MRR trong một lần gọi."""
        return {
            "hit_rate": self.calculate_hit_rate(expected_ids, retrieved_ids, top_k=3),
            "mrr": self.calculate_mrr(expected_ids, retrieved_ids),
            "retrieved_ids": retrieved_ids[:3],
        }

    async def evaluate_batch(self, dataset: List[Dict]) -> Dict:
        """
        Chạy eval cho toàn bộ bộ dữ liệu (không bắt buộc nếu dùng trong runner).
        """
        # Logic này thường được xử lý ở BenchmarkRunner để kết hợp với LLM Judge
        return {"note": "Use calculate methods directly in runner"}
