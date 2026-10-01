import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    explanation_backend: str = os.getenv("EXPLANATION_BACKEND", "local")
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    )
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "30000"))
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000")


settings = Settings()
