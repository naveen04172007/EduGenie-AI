# Implementation notes

## Mapping from supplied documentation

| Document requirement | Implementation |
|---|---|
| FastAPI backend | `main.py` |
| Q&A | `qna.py` + `/qa` |
| LaMini concept explanation | `explanation_module.py` + `/explain` |
| 3 MCQ quiz | `quiz_module.py` + `/quiz` |
| Summarization | `summary_module.py` + `/summarize` |
| Learning recommendations | `learning_path.py` + `/learn/recommendations` |
| HTML/CSS frontend | `templates/index.html`, `static/style.css` |
| Live form integration | `static/app.js` |
| Gemini integration | `services/gemini_service.py` |

## Current-model compatibility

The document names Gemini 1.5 Pro. Model availability changes over time, so the implementation exposes `GEMINI_MODEL` in `.env` rather than embedding an obsolete model identifier in application code. A current stable model can therefore be selected without changing the Python modules.

## Error handling

- Pydantic validates request sizes and required fields.
- Gemini configuration and generation errors are converted into useful server errors.
- Quiz JSON is cleaned of Markdown fences and validated against a Pydantic model.
- Local LaMini loading is lazy so the application can start without downloading the model immediately.
- If the local explanation model fails and a Gemini key exists, explanation falls back to Gemini.
