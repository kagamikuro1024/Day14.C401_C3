"""
Configuration constants for the AI Teaching Assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env theo thứ tự: thư mục agent/ trước, rồi thư mục root Lab14
# Để API key ở root Lab14 có thể ghi đè key cũ trong agent/.env
_ROOT_ENV = Path(__file__).parent.parent / ".env"
load_dotenv(_ROOT_ENV)   # Root Lab14 (.env mới nhất)
load_dotenv(override=False)  # agent/.env (chỉ nếu chưa có key)

# --- Paths ---
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
SLIDES_DIR = KNOWLEDGE_BASE_DIR / "slides"
CODE_SAMPLES_DIR = KNOWLEDGE_BASE_DIR / "code_samples"
FAISS_INDEX_DIR = BASE_DIR / "faiss_index"
FAQ_PATH = KNOWLEDGE_BASE_DIR / "faq.md"
COURSE_INFO_PATH = KNOWLEDGE_BASE_DIR / "course_info.json"

# --- OpenAI ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-5.4-nano"
LLM_TEMPERATURE = 0.3
EMBEDDING_MODEL = "text-embedding-3-large"

# --- RAG ---
CHUNK_SIZE = 512       # Giảm từ 1000 → embedding tập trung hơn, ít bị loãng
CHUNK_OVERLAP = 128    # ~25% overlap — đủ context bridge mà không thừa
RETRIEVAL_K = 6        # Tăng nhẹ để bù cho chunk nhỏ hơn

# --- Course ---
COURSE_NAME = "Lập trình C/C++ cơ bản"
