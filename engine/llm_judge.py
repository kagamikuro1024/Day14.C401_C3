import asyncio
import json
import os
import re
from typing import Dict, Any

from openai import AsyncOpenAI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

JUDGE_PROMPT_TEMPLATE = """Bạn là Review Agent chuyên đánh giá chất lượng AI Teaching Assistant cho khóa học C/C++.

CÂU HỎI CỦA HỌC VIÊN:
{question}

CÂU TRẢ LỜI GROUND TRUTH (kỳ vọng):
{ground_truth}

CÂU TRẢ LỜI CẦN ĐÁNH GIÁ:
{answer}

Hãy chấm điểm từ 1-5 cho 3 tiêu chí sau:
1. accuracy: Độ chính xác so với Ground Truth (1=sai hoàn toàn, 5=chính xác hoàn toàn).
2. completeness: Câu trả lời có đầy đủ các ý chính không (1=rất thiếu, 5=đầy đủ).
3. professionalism: Ngôn ngữ có đúng chuẩn Trợ giảng, thân thiện và không viết hộ bài không (1=kém, 5=xuất sắc).

Trả về kết quả dưới dạng JSON duy nhất, không thêm văn bản khác:
{{
  "accuracy": 5,
  "completeness": 5,
  "professionalism": 5,
  "reasoning": "giải thích ngắn gọn lý do chấm điểm"
}}"""

class LLMJudge:
    """Hệ thống đánh giá đa mô hình (GPT-4o & Gemini 1.5 Pro)."""

    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel("gemini-1.5-pro")

    def _parse_json_safely(self, text: str) -> Dict:
        """Trích xuất và parse JSON từ phản hồi của LLM."""
        try:
            # Tìm JSON bằng regex nếu model trả về kèm markdown
            match = re.search(r'\{(?:[^{}]|(?R))*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(text)
        except:
            return {"accuracy": 3, "completeness": 3, "professionalism": 3, "reasoning": "Failed to parse JSON"}

    async def judge_with_gpt4o(self, question: str, answer: str, ground_truth: str) -> Dict:
        """Chấm điểm bằng GPT-4o."""
        prompt = JUDGE_PROMPT_TEMPLATE.format(
            question=question, answer=answer, ground_truth=ground_truth
        )
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            data = json.loads(response.choices[0].message.content)
            # Lưu lại token usage để tính cost sau
            data["usage"] = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens
            }
            return data
        except Exception as e:
            return {"accuracy": 3, "reasoning": f"GPT error: {str(e)}", "usage": {"prompt_tokens": 0, "completion_tokens": 0}}

    async def judge_with_gemini(self, question: str, answer: str, ground_truth: str) -> Dict:
        """Chấm điểm bằng Gemini 1.5 Pro."""
        prompt = JUDGE_PROMPT_TEMPLATE.format(
            question=question, answer=answer, ground_truth=ground_truth
        )
        try:
            response = await asyncio.to_thread(
                self.gemini_model.generate_content,
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            data = self._parse_json_safely(response.text)
            # Gemini use response metadata for usage
            # Note: metadata might vary, this is a placeholder for actual billing logic
            data["usage"] = {
                "prompt_tokens": response.usage_metadata.prompt_token_count,
                "completion_tokens": response.usage_metadata.candidates_token_count
            }
            return data
        except Exception as e:
            return {"accuracy": 3, "reasoning": f"Gemini error: {str(e)}", "usage": {"prompt_tokens": 0, "completion_tokens": 0}}

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Thực hiện đánh giá song song bằng 2 mô hình và tính consensus.
        """
        gpt_task = self.judge_with_gpt4o(question, answer, ground_truth)
        gemini_task = self.judge_with_gemini(question, answer, ground_truth)
        
        gpt_res, gemini_res = await asyncio.gather(gpt_task, gemini_task)

        # Tính điểm trung bình
        avg_acc = (gpt_res["accuracy"] + gemini_res["accuracy"]) / 2
        avg_comp = (gpt_res["completeness"] + gemini_res["completeness"]) / 2
        avg_prof = (gpt_res["professionalism"] + gemini_res["professionalism"]) / 2
        
        final_score = (avg_acc + avg_comp + avg_prof) / 3

        # Tính độ đồng thuận (Agreement) dựa trên tiêu chí quan trọng nhất: Accuracy
        diff = abs(gpt_res["accuracy"] - gemini_res["accuracy"])
        agreement = max(0.0, 1.0 - (diff / 4.0)) # 1.0 nếu bằng nhau, 0.0 nếu lệch tối đa 4 điểm

        # Phát hiện xung đột (Conflict)
        conflict = diff > 1 # Nếu lệch trên 1.0 điểm thì coi là xung đột cao

        return {
            "final_score": round(final_score, 2),
            "agreement_rate": round(agreement, 2),
            "conflict_detected": conflict,
            "individual_scores": {
                "gpt-4o": gpt_res,
                "gemini-1.5-pro": gemini_res
            },
            "total_usage": {
                "openai": gpt_res["usage"],
                "gemini": gemini_res["usage"]
            }
        }
