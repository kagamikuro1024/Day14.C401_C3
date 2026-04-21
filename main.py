import asyncio
import json
import os
import sys
import codecs
import time

# Sửa lỗi Unicode trên Windows triệt để
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    except:
        pass

# Đảm bảo thư mục báo cáo tồn tại trước khi chạy (Tránh mất token nếu lỗi ghi file cuối cùng)
os.makedirs("reports", exist_ok=True)
print("[*] Reports directory ready.", flush=True)

# Đảm bảo các module bên trong agent/ có thể tìm thấy nhau
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agent"))

from engine.runner import BenchmarkRunner
from engine.llm_judge import LLMJudge
from main_agent import MainAgent

async def run_benchmark_with_results(agent_version: str):
    print(f"\n[*] Khoi dong Benchmark cho {agent_version}...", flush=True)

    # 1. Load Dataset
    if not os.path.exists("data/golden_set.jsonl"):
        print("[-] Loi: Thieu data/golden_set.jsonl. Hay chay enrichment truoc.")
        return None, None

    with open("data/golden_set.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    if not dataset:
        print("[-] Loi: File dataset rong.")
        return None, None

    # 2. Khởi tạo Pipeline thực tế
    agent = MainAgent()
    judge = LLMJudge()
    runner = BenchmarkRunner(agent, judge)
    
    # 3. Chạy toàn bộ (Batch Size 5 - an toàn tránh rate limit)
    results = await runner.run_all(dataset, batch_size=5)

    # 4. Tính toán Metrics tổng hợp
    valid_results = [r for r in results if r.get("status") != "error"]
    total_valid = len(valid_results)
    
    if total_valid == 0:
        return results, None

    avg_score = sum(r["judge"]["final_score"] for r in valid_results) / total_valid
    avg_hit_rate = sum(r["retrieval"]["hit_rate"] for r in valid_results) / total_valid
    avg_mrr = sum(r["retrieval"]["mrr"] for r in valid_results) / total_valid
    avg_lat = sum(r["latency"] for r in valid_results) / total_valid
    total_cost = sum(r.get("cost_usd", 0) for r in valid_results)
    avg_agreement = sum(r["judge"]["agreement_rate"] for r in valid_results) / total_valid

    summary = {
        "metadata": {
            "version": agent_version,
            "total_cases": len(results),
            "valid_cases": total_valid,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "metrics": {
            "avg_score": round(avg_score, 2),
            "hit_rate": round(avg_hit_rate, 2),
            "mrr": round(avg_mrr, 2),
            "latency_avg": round(avg_lat, 2),
            "agreement_rate": round(avg_agreement, 2)
        },
        "financials": {
            "total_cost_usd": round(total_cost, 4)
        }
    }
    
    return results, summary

async def main():
    v1_baseline_score = 3.8
    v2_results, v2_summary = await run_benchmark_with_results("Agent_V2_Production")
    
    if not v2_summary:
        print("[-] Loi: Khong the tao bao cao benchmark.")
        return

    # --- RELEASE GATE LOGIC (Standard ASCII) ---
    print("\n" + "="*50)
    print("--- KET QUA SO SANH & RELEASE GATE ---")
    print(f"V1 Baseline Score: {v1_baseline_score}")
    print(f"V2 Current Score:  {v2_summary['metrics']['avg_score']}")
    
    delta = v2_summary['metrics']['avg_score'] - v1_baseline_score
    print(f"Delta Performance: {'+' if delta >= 0 else ''}{delta:.2f}")
    
    print(f"\nRetrieval Metrics: Hit Rate @3: {v2_summary['metrics']['hit_rate']} | MRR: {v2_summary['metrics']['mrr']}")
    print(f"Judge Agreement : {v2_summary['metrics']['agreement_rate'] * 100}%")
    print(f"Total Cost (USD): ${v2_summary['financials']['total_cost_usd']}")
    print("="*50)

    # Decision Logic
    gate_passed = delta >= 0 and v2_summary['metrics']['avg_score'] >= 3.5
    
    if gate_passed:
        print("[OK] DECISION: RELEASE APPROVED (GATE PASSED)")
    else:
        if delta < 0:
            print("[!] DECISION: RELEASE BLOCKED (REGRESSION DETECTED)")
        else:
            print("[?] DECISION: RELEASE PENDING (SCORE TOO LOW)")

    # Lưu báo cáo
    os.makedirs("reports", exist_ok=True)
    with open("reports/summary.json", "w", encoding="utf-8") as f:
        json.dump(v2_summary, f, ensure_ascii=False, indent=2)
    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(v2_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n[DONE] Reports successfully saved to 'reports/' directory.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Benchmark interrupted by user.")
    except Exception as e:
        print(f"\n[!] Fatal error: {str(e)}")
