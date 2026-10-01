from functools import lru_cache

from config import settings
from services.gemini_service import GeminiConfigurationError, generate_text


@lru_cache(maxsize=1)
def _load_local_pipeline():
    from transformers import pipeline

    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        device=-1,
    )


def _local_explanation(topic: str) -> str:
    generator = _load_local_pipeline()
    prompt = (
        "Explain the following concept to a beginner. Use simple language, a short definition, "
        "an intuitive example, and 3 key points. Avoid unsupported claims.\n\nConcept: " + topic
    )
    result = generator(prompt, max_new_tokens=300, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_concept(topic: str) -> str:
    backend = settings.explanation_backend.lower()
    if backend == "gemini":
        return generate_text(
            f"Explain this educational concept to a beginner in simple language, with a definition, example, and 3 key points:\n{topic}",
            max_output_tokens=700,
        )

    if backend == "local":
        try:
            return _local_explanation(topic)
        except Exception as local_error:
            # A local model is intentionally optional. If it cannot load, use Gemini when configured.
            if settings.gemini_api_key:
                return generate_text(
                    f"Explain this educational concept to a beginner in simple language, with a definition, example, and 3 key points:\n{topic}",
                    max_output_tokens=700,
                )
            raise RuntimeError(
                "Local explanation model could not be loaded and GEMINI_API_KEY is not configured. "
                f"Original error: {local_error}"
            ) from local_error

    raise ValueError("EXPLANATION_BACKEND must be 'local' or 'gemini'.")
