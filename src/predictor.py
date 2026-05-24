from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import joblib

from src.config import (
    CATEGORY_MODEL_PATH,
    LABELS_PATH,
    LEVEL_MODEL_PATH,
    MODEL_DIR,
    VECTORIZER_PATH,
)
from src.preprocessing import clean_text


class JobOfferPredictor:
    BACKEND_HINTS = {
        "python",
        "django",
        "flask",
        "fastapi",
        "rest api",
        "restful api",
        "microservices",
        "postgresql",
        "mysql",
        "jwt",
        "authentication",
        "backend",
        "api",
    }
    DEVOPS_HINTS = {
        "aws",
        "azure",
        "gcp",
        "kubernetes",
        "terraform",
        "ci/cd",
        "monitoring",
        "cloud",
        "serverless",
        "lambda",
        "devops",
        "pipeline",
        "pipelines",
    }
    FRONTEND_HINTS = {
        "frontend",
        "front-end",
        "react",
        "typescript",
        "javascript",
        "html",
        "css",
        "next.js",
        "web ui",
        "user-facing",
    }
    DATA_HINTS = {
        "data engineer",
        "data engineering",
        "data analyst",
        "data scientist",
        "machine learning",
        "ml",
        "llm",
        "genai",
        "rag",
        "analytics",
        "data pipeline",
        "data pipelines",
        "etl",
        "elt",
        "spark",
        "databricks",
        "airflow",
        "pandas",
        "numpy",
        "statistics",
        "clickhouse",
        "big data",
    }
    OTHER_HINTS = {
        "marketing",
        "sales",
        "customer support",
        "recruiter",
        "hr",
        "operations",
        "business development",
        "content",
        "product manager",
        "project manager",
    }
    BACKEND_STRONG_HINTS = {
        "backend services",
        "backend development",
        "python backend",
        "fastapi",
        "flask",
        "django",
        "restful api",
        "restful apis",
        "rest api",
        "rest apis",
        "microservices",
        "postgresql",
        "mysql",
        "sqlalchemy",
    }
    DEVOPS_STRONG_HINTS = {
        "site reliability",
        "sre",
        "terraform",
        "prometheus",
        "grafana",
        "linux",
        "infrastructure",
        "observability",
        "networking",
        "deployment pipelines",
        "system reliability",
    }
    DATA_STRONG_HINTS = {
        "data engineer",
        "data engineering",
        "machine learning",
        "data pipelines",
        "data pipeline",
        "etl",
        "elt",
        "spark",
        "databricks",
        "airflow",
        "llm",
        "genai",
        "rag",
    }
    LEVEL_HINTS = {
        "internship": {"intern", "internship", "trainee", "student"},
        "junior": {"junior", "entry level", "entry-level", "graduate", "associate"},
        "regular": {"midlevel", "mid-level", "middle", "regular"},
        "senior": {"senior", "lead", "principal", "staff", "architect", "head of"},
    }
    EARLY_CAREER_HINTS = {
        "early-career",
        "early career",
        "start your journey",
        "grow your skills",
        "working student",
    }
    EXPERIENCE_STRENGTH_HINTS = {
        "strong experience",
        "very strong experience",
        "experienced",
        "production",
        "hands-on experience",
        "commercial experience",
        "5+ years",
        "4+ years",
        "3+ years",
    }

    def __init__(self, model_dir: str | Path | None = None) -> None:
        self.model_dir = Path(model_dir) if model_dir else MODEL_DIR
        self.vectorizer = joblib.load(self.model_dir / VECTORIZER_PATH.name)
        self.category_model = joblib.load(self.model_dir / CATEGORY_MODEL_PATH.name)
        self.level_model = joblib.load(self.model_dir / LEVEL_MODEL_PATH.name)

        labels_path = self.model_dir / LABELS_PATH.name
        if labels_path.exists():
            with labels_path.open("r", encoding="utf-8") as file:
                self.labels = json.load(file)
        else:
            self.labels = {}

    @staticmethod
    def _get_max_probability(model: Any, vectorized_text: Any) -> float:
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(vectorized_text)[0]
            return float(max(probabilities))
        return 1.0

    @staticmethod
    def _extract_years_of_experience(text: str) -> int | None:
        patterns = [
            r"(\d+)\s*\+?\s*years? of experience",
            r"(\d+)\s*\+?\s*years? experience",
            r"(\d+)\s*\+?\s*years? of [a-z\s/\-]{0,40}experience",
            r"(\d+)\s*\+?\s*years? in [a-z\s/\-]{0,40}",
            r"(\d+)\s*\+?\s*years? of [a-z\s/\-]{0,40}development",
            r"minimum of (\d+)\s*years?",
            r"at least (\d+)\s*years?",
            r"minimum (\d+)\s*years?",
            r"(\d+)\s*\+?\s*yoe\b",
        ]

        lowered = text.lower()
        for pattern in patterns:
            match = re.search(pattern, lowered)
            if match:
                return int(match.group(1))
        return None

    @staticmethod
    def _level_from_years(years: int) -> str:
        if years <= 0:
            return "internship"
        if years <= 2:
            return "junior"
        if years <= 4:
            return "regular"
        return "senior"

    def _adjust_level_with_years(self, text: str, predicted_level: str) -> str:
        years = self._extract_years_of_experience(text)
        if years is None:
            return predicted_level
        return self._level_from_years(years)

    @staticmethod
    def _looks_like_full_engineering_role(text: str) -> bool:
        engineering_markers = {
            "engineer",
            "developer",
            "backend",
            "api",
            "production",
            "ci/cd",
            "docker",
            "kubernetes",
            "fastapi",
            "flask",
            "django",
            "linux",
            "terraform",
            "spark",
            "airflow",
        }
        return sum(1 for marker in engineering_markers if marker in text) >= 3

    @staticmethod
    def _contains_phrase(text: str, phrase: str) -> bool:
        pattern = r"\b" + re.escape(phrase.lower()) + r"\b"
        return re.search(pattern, text.lower()) is not None

    @classmethod
    def _extract_level_from_keywords(cls, text: str) -> str | None:
        lowered = text.lower()

        if any(cls._contains_phrase(lowered, hint) for hint in cls.EARLY_CAREER_HINTS):
            return "junior"

        for keyword in cls.LEVEL_HINTS["internship"]:
            if cls._contains_phrase(lowered, keyword):
                return "internship"

        if any(cls._contains_phrase(lowered, keyword) for keyword in cls.LEVEL_HINTS["senior"]):
            if "not for seniors" not in lowered and "working closely with our senior" not in lowered:
                return "senior"

        if any(cls._contains_phrase(lowered, keyword) for keyword in cls.LEVEL_HINTS["junior"]):
            if any(cls._contains_phrase(lowered, keyword) for keyword in cls.LEVEL_HINTS["regular"]):
                return "regular"
            return "junior"

        if any(cls._contains_phrase(lowered, keyword) for keyword in cls.LEVEL_HINTS["regular"]):
            return "regular"

        return None

    def _adjust_level(self, text: str, predicted_level: str) -> str:
        lowered = text.lower()
        keyword_level = self._extract_level_from_keywords(text)
        if keyword_level:
            return keyword_level
        years_level = self._adjust_level_with_years(text, predicted_level)
        if years_level != predicted_level:
            return years_level

        if any(hint in lowered for hint in self.EARLY_CAREER_HINTS):
            return "junior"

        if predicted_level == "junior":
            if any(hint in lowered for hint in self.EXPERIENCE_STRENGTH_HINTS):
                return "regular"

        if predicted_level == "internship":
            if any(hint in lowered for hint in self.EXPERIENCE_STRENGTH_HINTS):
                return "regular"
            if self._looks_like_full_engineering_role(lowered):
                return "regular"

        return predicted_level

    @classmethod
    def _count_hints(cls, text: str, hints: set[str]) -> int:
        return sum(1 for hint in hints if hint in text)

    @classmethod
    def _weighted_score(cls, text: str, base_hints: set[str], strong_hints: set[str]) -> int:
        base_score = cls._count_hints(text, base_hints)
        strong_score = cls._count_hints(text, strong_hints) * 2
        return base_score + strong_score

    def _score_categories(self, cleaned_text: str) -> dict[str, int]:
        return {
            "backend": self._weighted_score(cleaned_text, self.BACKEND_HINTS, self.BACKEND_STRONG_HINTS),
            "frontend": self._count_hints(cleaned_text, self.FRONTEND_HINTS),
            "data": self._weighted_score(cleaned_text, self.DATA_HINTS, self.DATA_STRONG_HINTS),
            "devops": self._weighted_score(cleaned_text, self.DEVOPS_HINTS, self.DEVOPS_STRONG_HINTS),
            "other": self._count_hints(cleaned_text, self.OTHER_HINTS),
        }

    def _adjust_category_with_keywords(self, cleaned_text: str, predicted_category: str) -> str:
        scores = self._score_categories(cleaned_text)
        backend_hits = scores["backend"]
        devops_hits = scores["devops"]
        data_hits = scores["data"]
        frontend_hits = scores["frontend"]

        if "data engineer" in cleaned_text or "data engineering" in cleaned_text:
            return "data"

        if "devops" in cleaned_text or "site reliability" in cleaned_text or "sre" in cleaned_text:
            return "devops"

        if "frontend" in cleaned_text or "front-end" in cleaned_text:
            return "frontend"

        if "backend" in cleaned_text or "back-end" in cleaned_text:
            if backend_hits >= data_hits:
                return "backend"

        if data_hits >= 6 and data_hits >= backend_hits + 2 and data_hits >= devops_hits:
            return "data"

        if frontend_hits >= 3 and frontend_hits >= backend_hits and frontend_hits >= data_hits:
            return "frontend"

        if devops_hits >= 6 and devops_hits >= backend_hits + 2 and devops_hits >= data_hits:
            return "devops"

        # Mixed cloud/platform vacancies often contain both backend and devops signals.
        if backend_hits >= 4 and backend_hits >= devops_hits and "python" in cleaned_text:
            return "backend"

        if backend_hits >= 6 and "python" in cleaned_text:
            return "backend"

        if backend_hits >= 5 and "rest" in cleaned_text and "api" in cleaned_text:
            return "backend"

        if data_hits >= 5 and "data" in cleaned_text and "pipeline" in cleaned_text:
            return "data"

        if devops_hits >= 5 and ("linux" in cleaned_text or "infrastructure" in cleaned_text):
            return "devops"

        if backend_hits >= 5 and "python" in cleaned_text:
            return "backend"

        return predicted_category

    def predict(self, text: str) -> dict[str, Any]:
        cleaned_text = clean_text(text)
        if not cleaned_text:
            raise ValueError("Text must not be empty.")

        vectorized_text = self.vectorizer.transform([cleaned_text])
        predicted_category = self.category_model.predict(vectorized_text)[0]
        category = self._adjust_category_with_keywords(cleaned_text, predicted_category)
        predicted_level = self.level_model.predict(vectorized_text)[0]
        level = self._adjust_level(text, predicted_level)

        category_confidence = self._get_max_probability(self.category_model, vectorized_text)
        level_confidence = self._get_max_probability(self.level_model, vectorized_text)
        confidence = round((category_confidence + level_confidence) / 2, 4)

        recommended = category == "backend" and level in {"internship", "junior"}

        return {
            "category": category,
            "level": level,
            "confidence": confidence,
            "recommended": recommended,
        }


def predict_job_offer(text: str, model_dir: str | Path | None = None) -> dict[str, Any]:
    predictor = JobOfferPredictor(model_dir=model_dir)
    return predictor.predict(text)
