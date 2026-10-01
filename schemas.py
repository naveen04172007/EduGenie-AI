from pydantic import BaseModel, Field, field_validator

from config import settings


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=settings.max_input_chars)

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Input cannot be empty")
        return value


class QuizRequest(TextRequest):
    num_questions: int = Field(default=3, ge=1, le=10)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: str = Field(default="beginner", min_length=1, max_length=50)

    @field_validator("topic", "level")
    @classmethod
    def clean(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty")
        return value


class TextResponse(BaseModel):
    result: str


class QAResponse(BaseModel):
    answer: str


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str = ""


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]
