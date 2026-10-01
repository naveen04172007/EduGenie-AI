from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

from config import settings
from schemas import (
    TextRequest,
    QuizRequest,
    LearningPathRequest,
    QAResponse,
    QuizResponse,
    TextResponse,
)
from qna import answer_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(
    title="EduGenie",
    description="Google Gemini powered learning assistant with optional local LaMini explanation model.",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa", response_model=QAResponse)
async def qa(payload: TextRequest):
    return {"answer": answer_question(payload.text)}


@app.post("/explain", response_model=TextResponse)
async def explain(payload: TextRequest):
    return {"result": explain_concept(payload.text)}


@app.post("/quiz", response_model=QuizResponse)
async def quiz(payload: QuizRequest):
    return {"questions": generate_quiz(payload.text, payload.num_questions)}


@app.post("/summarize", response_model=TextResponse)
async def summarize(payload: TextRequest):
    return {"result": summarize_text(payload.text)}


@app.post("/learn/recommendations", response_model=TextResponse)
async def learning_recommendations(payload: LearningPathRequest):
    return {"result": get_learning_recommendations(payload.topic, payload.level)}
