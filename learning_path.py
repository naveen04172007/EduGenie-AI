from services.gemini_service import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""Create a structured learning path for the topic: {topic}
Learner level: {level}

Include:
1. A short goal statement.
2. Beginner, intermediate, and advanced stages.
3. For each stage: concepts, suggested sequence, practice activities, and an approximate timeline.
4. Recommended resource types (videos, documentation/articles, books, practice sites). Do not fabricate exact URLs.
5. A simple weekly study routine.
6. A checkpoint project or assessment.

Make the plan realistic, concise, and adaptable. Clearly label any suggested timeline as approximate.
"""
    return generate_text(prompt, max_output_tokens=1800)
