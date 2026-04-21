"""
Multi-Judge Engine — GPT-4o-mini + GPT-5.4-mini.
Tính toán độ đồng thuận và xử lý xung đột tự động.
"""
import asyncio
import json
import os
import re
from typing import Dict, Any
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

JUDGE_PROMPT_TEMPLATE = """Bạn là Review Agent chuyên đánh giá chất lượng AI Teaching Assistant cho khóa học C/C++.

CÂU HỎI CỦA HỌC VIÊN:
{question}

CÂU TRẢ LỜI GROUND TRUTH (kỳ vọng):
{ground_truth}

CÂU TRẢ LỜI CẦN ĐÁNH GIÁ:
{answer}

Chấm điểm từ 1-5 cho từng tiêu chí:
- accuracy: Độ chính xác với Ground Truth (1=sai hoàn toàn, 5=chính xác hoàn toàn)
- completeness: Câu trả lời đầy đủ không (1=rất thiếu, 5=đầy đủ)
- professionalism: Ngôn ngữ đúng chuẩn TA không (1=rất kém, 5=xuất sắc)

Trả về JSON (chỉ JSON, không có text thêm):
{{"accuracy": X, "completeness": X, "professionalism": X, "reasoning": "lý do ngắn gọn"}}"""


class LLMJudge:
    """Multi-Judge sử dụng GPT-4o-mini và GPT-5.4-mini."""

    JUDGE_MODELS = {
        "judge_1": "gpt-4o-mini",
        "judge_2": "gpt-5.4-mini",
    }

    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print(f"[OK] Multi-Judge Ready: {self.JUDGE_MODELS['judge_1']} + {self.JUDGE_MODELS['judge_2']}", flush=True)

    def _parse_json_safely(self, text: str) -> Dict:
        """Parse JSON an toàn - xử lý cả trường hợp có markdown wrapper."""
        try:
            # Thử parse trực tiếp
            return json.loads(text)
        except:
            pass
        try:
            # Tìm JSON trong text (xử lý markdown ```json ... ```)
            match = re.search(r'\{[^{}]+\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except:
            pass
        # Fallback mặc định khi không parse được
        return {
            "accuracy": 3,
            "completeness": 3,
            "professionalism": 3,
            "reasoning": f"Failed to parse response: {text[:100]}"
        }

    async def _call_judge(self, model: str, question: str, answer: str, ground_truth: str) -> Dict:
        """Gọi một model làm judge."""
        prompt = JUDGE_PROMPT_TEMPLATE.format(
            question=question,
            answer=answer,
            ground_truth=ground_truth
        )
        try:
            response = await self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            data = self._parse_json_safely(response.choices[0].message.content)
            data["usage"] = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
            }
            return data
        except Exception as e:
            return {
                "accuracy": 3,
                "completeness": 3,
                "professionalism": 3,
                "reasoning": f"Error ({model}): {str(e)}",
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
                "error": True,
            }

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Chạy 2 judges song song, tính consensus, xử lý conflict.

        Logic:
        - Đồng thuận: |accuracy_A - accuracy_B| <= 1 → dùng average
        - Xung đột: |accuracy_A - accuracy_B| > 1 → đánh dấu conflict_detected
        """
        model_1 = self.JUDGE_MODELS["judge_1"]
        model_2 = self.JUDGE_MODELS["judge_2"]

        res_1, res_2 = await asyncio.gather(
            self._call_judge(model_1, question, answer, ground_truth),
            self._call_judge(model_2, question, answer, ground_truth),
        )

        # Tính điểm tổng hợp cho từng judge
        avg_1 = (res_1.get("accuracy", 3) + res_1.get("completeness", 3) + res_1.get("professionalism", 3)) / 3
        avg_2 = (res_2.get("accuracy", 3) + res_2.get("completeness", 3) + res_2.get("professionalism", 3)) / 3
        final_score = (avg_1 + avg_2) / 2

        # Tính agreement dựa trên accuracy (tiêu chí quan trọng nhất)
        diff = abs(res_1.get("accuracy", 3) - res_2.get("accuracy", 3))
        agreement_rate = max(0.0, 1.0 - diff / 4.0)
        conflict = diff > 1

        return {
            "final_score": round(final_score, 2),
            "agreement_rate": round(agreement_rate, 2),
            "conflict_detected": conflict,
            "needs_human_review": conflict,
            "individual_scores": {
                model_1: round(avg_1, 2),
                model_2: round(avg_2, 2),
            },
            "detailed_scores": {
                model_1: {k: v for k, v in res_1.items() if k not in ("usage",)},
                model_2: {k: v for k, v in res_2.items() if k not in ("usage",)},
            },
            "total_usage": {
                model_1: res_1.get("usage", {}),
                model_2: res_2.get("usage", {}),
            },
        }
