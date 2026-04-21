"""
Configuration constants for the AI Teaching Assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

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
LLM_MODEL = "gpt-4o"
LLM_TEMPERATURE = 0.3
EMBEDDING_MODEL = "text-embedding-3-large"

# --- RAG ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
RETRIEVAL_K = 5  # Number of documents to retrieve

# --- Course ---
COURSE_NAME = "Lập trình C/C++ cơ bản"
