"""
Multi-Judge Engine — GPT-4o + Gemini-2.5-Pro Consensus System.

Hệ thống sử dụng 2 model LLM làm "thẩm phán" độc lập để đánh giá
chất lượng câu trả lời của AI TA, sau đó tính toán độ đồng thuận
và xử lý xung đột tự động.
"""
import asyncio
import json
import os
from typing import Dict, Any, Optional

from openai import AsyncOpenAI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# === PROMPT TEMPLATE CHO JUDGE ===
JUDGE_PROMPT = """Bạn là AI Review Expert đánh giá chất lượng AI Teaching Assistant (TA).

CÂU HỎI CỦA HỌC VIÊN:
{question}

CÂU TRẢ LỜI CHUẨN (Ground Truth — câu trả lời kỳ vọng):
{ground_truth}

CÂU TRẢ LỜI CẦN ĐÁNH GIÁ (AI TA đã trả lời):
{answer}

Hãy chấm điểm từ 1 đến 5 cho từng tiêu chí dưới đây:

1. **accuracy** (1-5): Câu trả lời có chính xác, phù hợp với Ground Truth không?
   - 1 = Hoàn toàn sai / không liên quan
   - 3 = Đúng một phần
   - 5 = Chính xác hoàn toàn

2. **completeness** (1-5): Câu trả lời có đầy đủ thông tin không?
   - 1 = Rất thiếu, bỏ sót nhiều
   - 3 = Có đủ ý chính nhưng còn thiếu chi tiết
   - 5 = Đầy đủ và chi tiết

3. **professionalism** (1-5): Ngôn ngữ, giọng điệu có phù hợp với TA không?
   - 1 = Không chuyên nghiệp, sai giọng điệu
   - 3 = Chấp nhận được
   - 5 = Rất chuyên nghiệp, thân thiện, đúng Socratic Method

Trả về JSON (chỉ JSON, không markdown, không text thêm):
{{"accuracy": X, "completeness": X, "professionalism": X, "reasoning": "lý do đánh giá ngắn gọn (< 100 từ)"}}"""


class LLMJudge:
    """
    Multi-Judge sử dụng GPT-4o và Gemini-2.5-Pro.
    
    Đặc điểm:
    - Chạy 2 judges song song (async)
    - Tính agreement rate tự động
    - Phát hiện và xử lý xung đột (khi điểm lệch > 1)
    - Có position bias detection (nâng cao)
    """

    def __init__(self):
        """Khởi tạo clients cho cả 2 judge models."""
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
        # Rubrics tham chiếu — dùng để document scoring criteria
        self.rubrics = {
            "accuracy": "Chấm điểm 1-5 dựa trên độ chính xác so với Ground Truth",
            "completeness": "Chấm điểm 1-5 dựa trên mức độ đầy đủ của câu trả lời",
            "professionalism": "Chấm điểm 1-5 dựa trên sự chuyên nghiệp và đúng phong cách TA",
        }

    async def judge_with_gpt4o(
        self, 
        question: str, 
        answer: str, 
        ground_truth: str
    ) -> Dict[str, Any]:
        """
        Gọi GPT-4o đánh giá chất lượng câu trả lời.
        
        Returns:
            Dict với accuracy, completeness, professionalism (1-5), reasoning
        """
        prompt = JUDGE_PROMPT.format(
            question=question,
            answer=answer,
            ground_truth=ground_truth,
        )
        
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.1,  # Thấp → consistent hơn
                max_tokens=300,
            )
            result = json.loads(response.choices[0].message.content)
            result["judge_model"] = "gpt-4o"
            result["error"] = False
            return result
            
        except Exception as e:
            return {
                "accuracy": 3, "completeness": 3, "professionalism": 3,
                "reasoning": f"GPT-4o error: {str(e)[:100]}",
                "judge_model": "gpt-4o",
                "error": True,
            }

    async def judge_with_gemini(
        self, 
        question: str, 
        answer: str, 
        ground_truth: str
    ) -> Dict[str, Any]:
        """
        Gọi Gemini-2.5-Pro đánh giá chất lượng câu trả lời.
        
        Returns:
            Dict với accuracy, completeness, professionalism (1-5), reasoning
        """
        prompt = JUDGE_PROMPT.format(
            question=question,
            answer=answer,
            ground_truth=ground_truth,
        )
        
        try:
            model = genai.GenerativeModel("gemini-2.5-pro-preview-05-06")
            # Dùng asyncio.to_thread vì Gemini SDK là sync
            response = await asyncio.to_thread(
                model.generate_content,
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.1,
                    max_output_tokens=300,
                )
            )
            
            # Xử lý response text (có thể có markdown)
            text = response.text.strip()
            if "```" in text:
                # Loại bỏ ```json ... ```
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:].strip()
            
            result = json.loads(text)
            result["judge_model"] = "gemini-2.5-pro"
            result["error"] = False
            return result
            
        except Exception as e:
            return {
                "accuracy": 3, "completeness": 3, "professionalism": 3,
                "reasoning": f"Gemini error: {str(e)[:100]}",
                "judge_model": "gemini-2.5-pro",
                "error": True,
            }

    def _calculate_agreement(self, score_a: float, score_b: float) -> float:
        """
        Tính agreement rate giữa 2 judges.
        
        Logic:
        - |diff| == 0 → agreement = 1.0
        - |diff| == 1 → agreement = 0.75 (minor disagreement)
        - |diff| == 2 → agreement = 0.5 (moderate disagreement)
        - |diff| > 2 → agreement < 0.5 (major disagreement — conflict!)
        """
        diff = abs(score_a - score_b)
        agreement = max(0.0, 1.0 - diff / 4.0)
        return round(agreement, 3)

    async def evaluate_multi_judge(
        self, 
        question: str, 
        answer: str, 
        ground_truth: str
    ) -> Dict[str, Any]:
        """
        Chạy 2 judges song song, tính consensus, xử lý conflict.
        
        Logic conflict resolution:
        - |accuracy_score difference| <= 1: ĐỒNG THUẬN → dùng average
        - |accuracy_score difference| > 1: XUNG ĐỘT → đánh dấu needs_human_review
        
        Returns:
            Dict đầy đủ gồm final_score, agreement_rate, conflict info, individual scores
        """
        # Chạy 2 judges song song (không chờ nhau)
        gpt_result, gemini_result = await asyncio.gather(
            self.judge_with_gpt4o(question, answer, ground_truth),
            self.judge_with_gemini(question, answer, ground_truth),
        )

        # Lấy điểm accuracy của từng judge (tiêu chí quan trọng nhất)
        gpt_accuracy = gpt_result.get("accuracy", 3)
        gemini_accuracy = gemini_result.get("accuracy", 3)
        
        # Tính điểm tổng hợp cho mỗi judge (trung bình 3 tiêu chí)
        def avg_score(result: Dict) -> float:
            return (
                result.get("accuracy", 3) + 
                result.get("completeness", 3) + 
                result.get("professionalism", 3)
            ) / 3

        gpt_avg = avg_score(gpt_result)
        gemini_avg = avg_score(gemini_result)
        
        # Final score = trung bình của 2 judges
        final_score = (gpt_avg + gemini_avg) / 2
        
        # Tính agreement dựa trên accuracy score
        accuracy_diff = abs(gpt_accuracy - gemini_accuracy)
        agreement_rate = self._calculate_agreement(gpt_accuracy, gemini_accuracy)
        conflict_detected = accuracy_diff > 1

        return {
            "final_score": round(final_score, 2),
            "agreement_rate": agreement_rate,
            "conflict_detected": conflict_detected,
            "needs_human_review": conflict_detected,
            "accuracy_score_diff": accuracy_diff,
            "individual_scores": {
                "gpt-4o": round(gpt_avg, 2),
                "gemini-2.5-pro": round(gemini_avg, 2),
            },
            "detailed_criteria": {
                "gpt-4o": {
                    "accuracy": gpt_result.get("accuracy", 3),
                    "completeness": gpt_result.get("completeness", 3),
                    "professionalism": gpt_result.get("professionalism", 3),
                    "error": gpt_result.get("error", False),
                },
                "gemini-2.5-pro": {
                    "accuracy": gemini_result.get("accuracy", 3),
                    "completeness": gemini_result.get("completeness", 3),
                    "professionalism": gemini_result.get("professionalism", 3),
                    "error": gemini_result.get("error", False),
                },
            },
            "reasoning": {
                "gpt-4o": gpt_result.get("reasoning", ""),
                "gemini-2.5-pro": gemini_result.get("reasoning", ""),
            },
        }

    async def check_position_bias(
        self, 
        question: str,
        response_a: str, 
        response_b: str,
        ground_truth: str
    ) -> Dict[str, Any]:
        """
        Kiểm tra Position Bias: đổi thứ tự A/B, xem điểm có thay đổi không.
        
        Nếu judge cho A > B khi A ở vị trí đầu, nhưng B > A khi B ở vị trí đầu
        → Judge có position bias (thiên vị về vị trí).
        """
        # Đánh giá thứ tự gốc: A trước B
        score_ab_a, score_ab_b = await asyncio.gather(
            self.judge_with_gpt4o(question, response_a, ground_truth),
            self.judge_with_gpt4o(question, response_b, ground_truth),
        )
        
        # Đánh giá thứ tự đổi: B trước A  
        score_ba_b, score_ba_a = await asyncio.gather(
            self.judge_with_gpt4o(question, response_b, ground_truth),
            self.judge_with_gpt4o(question, response_a, ground_truth),
        )

        # So sánh điểm A khi ở vị trí "đầu" vs "sau"
        a_first_score = score_ab_a.get("accuracy", 3)
        a_second_score = score_ba_a.get("accuracy", 3)
        bias_score_a = abs(a_first_score - a_second_score)

        return {
            "bias_detected": bias_score_a > 0.5,
            "bias_magnitude": bias_score_a,
            "score_a_when_first": a_first_score,
            "score_a_when_second": a_second_score,
            "interpretation": "Có position bias" if bias_score_a > 0.5 else "Không phát hiện position bias",
        }