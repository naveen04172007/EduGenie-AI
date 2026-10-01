# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project document. It provides:

- Question answering (`/qa`)
- Concept explanation (`/explain`)
- MCQ quiz generation (`/quiz`)
- Passage summarization (`/summarize`)
- Structured learning recommendations (`/learn/recommendations`)

The original document describes FastAPI, an HTML/CSS frontend, Gemini 1.5 Pro for cloud tasks, and LaMini-Flan-T5-783M for explanations. This implementation keeps that modular design but uses Google's current `google-genai` Python SDK and makes the Gemini model configurable through `.env`.

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── schemas.py
├── qna.py
├── explanation_module.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── services/
│   └── gemini_service.py
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
├── tests/
│   ├── test_api.py
│   └── test_modules.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 1. Install Python

Use Python 3.10 or newer. Verify:

```bash
python --version
```

On Windows, `py --version` is also useful.

## 2. Open in VS Code

1. Extract/open the `EduGenie` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create a virtual environment:

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> The local LaMini model uses PyTorch and Transformers, so the first installation can be large. The first explanation request can also download the model from Hugging Face.

## 3. Configure Gemini

Create a Google AI Studio API key, then copy `.env.example` to `.env` and set:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.8-flash
EXPLANATION_BACKEND=local
```

If you want every feature to use Gemini instead of downloading the local LaMini model:

```env
EXPLANATION_BACKEND=gemini
```

Do not commit `.env` to Git.

## 4. Run

From the project root:

```bash
uvicorn main:app --reload
```

Open:

- http://127.0.0.1:8000 — web application
- http://127.0.0.1:8000/docs — interactive FastAPI API documentation
- http://127.0.0.1:8000/health — health check

## 5. Test

Run the automated tests:

```bash
pytest -q
```

The tests mock model calls, so they do not require an API key or an internet connection.

## 6. Test each feature manually

### Q&A
Select **Ask a Question** and enter:

```text
Which is the largest ocean?
```

### Explanation
Select **Explain a Concept** and enter:

```text
Pythagoras theorem
```

### Quiz
Select **Generate Quiz**, paste a passage, choose 3 questions, and submit.

### Summary
Paste a long educational passage and select **Summarize Text**.

### Learning path
Select **Learning Path**, enter `SQL`, and choose a level.

## API examples

Q&A:

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"What is photosynthesis?\"}"
```

Quiz:

```bash
curl -X POST http://127.0.0.1:8000/quiz ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"Water boils at 100 degrees Celsius at standard atmospheric pressure.\",\"num_questions\":3}"
```

On macOS/Linux, replace `^` with `\` for line continuation, or place the command on one line.

## Troubleshooting

### `GEMINI_API_KEY is not configured`
Create `.env` from `.env.example` and add the API key. Restart Uvicorn after changing `.env`.

### Local explanation model fails to load
Use:

```env
EXPLANATION_BACKEND=gemini
```

Then restart the server. This avoids the local Transformers/PyTorch model and uses Gemini for explanations.

### API quota/model error
Change `GEMINI_MODEL` to a model currently available to your API key. The model is deliberately configurable rather than hard-coded.

### PowerShell blocks activation
You can run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## Design notes

The supplied documentation lists the REST endpoints `/qa`, `/explain`, `/quiz`, `/summarize`, and `/learn/recommendations`, and describes the frontend as a task dropdown, text area, submit button, and result area. This implementation retains that flow while adding validation, structured Pydantic responses, error handling, tests, and a health endpoint.
