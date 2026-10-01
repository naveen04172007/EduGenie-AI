from schemas import QuizQuestion
from services.gemini_service import generate_json


def generate_quiz(text: str, num_questions: int = 3) -> list[QuizQuestion]:
    prompt = f"""Generate exactly {num_questions} multiple-choice questions from the passage below.
Return ONLY valid JSON in this exact shape:
{{"questions":[{{"question":"...","options":["A","B","C","D"],"correct_answer":"...","explanation":"..."}}]}}

Rules:
- Every question must be answerable from the passage.
- Every question must have exactly four distinct options.
- correct_answer must exactly match one option string.
- Explanations should briefly say why the correct option is correct.
- Do not include markdown or extra keys.

PASSAGE:
{text}
"""
    data = generate_json(prompt)
    if not isinstance(data, dict) or not isinstance(data.get("questions"), list):
        raise ValueError("Quiz response did not contain a questions list.")
    questions = []
    for item in data["questions"][:num_questions]:
        questions.append(QuizQuestion.model_validate(item))
    if len(questions) != num_questions:
        raise ValueError("The model did not generate the requested number of questions.")
    return questions
