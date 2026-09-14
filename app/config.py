import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


class Settings:
    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Qdrant
    QDRANT_URL = os.getenv("QDRANT_CLUSTER_ENDPOINT")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = "enterprise_rag"

    # Groq
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_API_KEY = os.getenv("GROQ_FALLBACK_API_KEY")


# Global settings object
settings = Settings()