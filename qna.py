from services.gemini_service import generate_text


def answer_question(question: str) -> str:
    prompt = f"""You are EduGenie, an educational assistant. Answer the student's question accurately and concisely.
Explain unfamiliar terms briefly when useful. If the question is ambiguous, state the assumption you used.
Do not invent sources or facts. Prefer a clear answer followed by a short explanation.

Student question:
{question}
"""
    return generate_text(prompt, max_output_tokens=900)
