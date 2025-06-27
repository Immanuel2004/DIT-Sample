import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3-8b-8192")
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", 0.3))

DEFAULT_SAMPLE_SIZE = int(os.getenv("DEFAULT_SAMPLE_SIZE", 1000))

if not GROQ_API_KEY or "xxxx" in GROQ_API_KEY.lower():
    raise ValueError("🚨 Missing or invalid GROQ_API_KEY in .env")
