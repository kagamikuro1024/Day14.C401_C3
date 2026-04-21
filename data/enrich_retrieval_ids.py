"""
Enrich golden_set.jsonl bằng cách điền expected_retrieval_ids
thực tế từ FAISS (top-3 chunks liên quan nhất cho mỗi câu hỏi).

Chạy: python data/enrich_retrieval_ids.py
"""
import json
import sys
import os

# Thêm agent vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "agent"))

from rag.retriever import search_documents


def enrich(input_path="data/golden_set.jsonl", output_path="data/golden_set.jsonl"):
    with open(input_path, encoding="utf-8") as f:
        cases = [json.loads(l) for l in f if l.strip()]

    print(f"[*] Enriching {len(cases)} cases with retrieval IDs...")
    enriched = []

    for i, case in enumerate(cases):
        if i % 20 == 0:
            print(f"  [>] Progress: {i}/{len(cases)}...")
        try:
            docs = search_documents(case["question"], k=3)
            ids = [
                d.metadata.get("chunk_id", f"unknown_{j}")
                for j, d in enumerate(docs)
            ]
            case["expected_retrieval_ids"] = ids
        except Exception as e:
            print(f"  [!] Error at case {i}: {e}")
            case["expected_retrieval_ids"] = []
        enriched.append(case)

    with open(output_path, "w", encoding="utf-8") as f:
        for case in enriched:
            f.write(json.dumps(case, ensure_ascii=False) + "\n")

    filled = sum(1 for c in enriched if c.get("expected_retrieval_ids"))
    print(f"[+] Done! {filled}/{len(enriched)} cases co expected_retrieval_ids.")


if __name__ == "__main__":
    enrich()
