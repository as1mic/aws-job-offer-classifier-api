from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.requests import Request

from src.predictor import predict_job_offer


BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title="AWS Job Offer Classifier API",
    description="Local web demo for classifying IT job offers.",
    version="1.0.0",
)


class PredictionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Job offer text to classify.")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "request": request,
            "example_text": (
                "We are looking for a Junior Python Backend Developer with FastAPI, "
                "SQL, Docker and REST API experience."
            ),
        },
    )


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/predict")
async def predict(payload: PredictionRequest) -> dict[str, str | float | bool]:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text must not be empty.")

    try:
        return predict_job_offer(text)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="Internal prediction error.") from error