from services.gemini_service import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""Summarize the educational passage below for a student revising for an exam.
Keep the important facts, relationships, definitions, and conclusions. Remove repetition.
Use plain language and short paragraphs or bullets. Do not add information that is not supported by the passage.

PASSAGE:
{text}
"""
    return generate_text(prompt, max_output_tokens=1000)
