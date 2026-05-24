import json
from pathlib import Path

import pytest

from src.predictor import JobOfferPredictor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "model"


@pytest.fixture
def predictor():
    expected_files = [
        MODEL_DIR / "vectorizer.joblib",
        MODEL_DIR / "category_model.joblib",
        MODEL_DIR / "level_model.joblib",
        MODEL_DIR / "labels.json",
    ]
    missing = [str(path.name) for path in expected_files if not path.exists()]
    if missing:
        pytest.skip(f"Missing trained model artifacts: {json.dumps(missing)}")
    return JobOfferPredictor(model_dir=MODEL_DIR)


def test_predictor_returns_expected_keys(predictor):
    result = predictor.predict("Junior Python Backend Developer with FastAPI and SQL")

    assert set(result.keys()) == {"category", "level", "confidence", "recommended"}
    assert isinstance(result["confidence"], float)


def test_recommended_logic_for_backend_junior(predictor):
    result = predictor.predict("Junior Backend Developer with Python FastAPI SQL Docker")

    assert result["category"] == "backend"
    assert result["level"] in {"junior", "internship"}
    assert result["recommended"] is True


def test_years_of_experience_adjusts_level(predictor):
    result = predictor.predict(
        "Backend Engineer with 5+ years of experience in Python, REST APIs, AWS Lambda and PostgreSQL"
    )

    assert result["category"] == "backend"
    assert result["level"] == "senior"
    assert result["recommended"] is False


def test_development_experience_phrase_adjusts_level(predictor):
    result = predictor.predict(
        "Senior Python Engineer with 5+ years of Python development experience, FastAPI, PostgreSQL and AWS"
    )

    assert result["level"] == "senior"


def test_backend_keywords_can_override_devops_like_text(predictor):
    result = predictor.predict(
        "Python backend engineer building FastAPI microservices, REST APIs, PostgreSQL and AWS Lambda in cloud environments"
    )

    assert result["category"] == "backend"


def test_explicit_junior_keyword_adjusts_level(predictor):
    result = predictor.predict(
        "Junior software engineer with Python, Docker, AWS Lambda and SQL experience"
    )

    assert result["level"] == "junior"


def test_midlevel_keyword_adjusts_level_to_regular(predictor):
    result = predictor.predict(
        "This job is for junior to midlevel engineers, not for seniors. Python, Docker, AWS and Terraform."
    )

    assert result["level"] == "regular"


def test_data_engineer_phrase_adjusts_category(predictor):
    result = predictor.predict(
        "Junior Data Engineer with Python, SQL, ETL, Airflow, Spark and cloud data pipelines"
    )

    assert result["category"] == "data"


def test_experienced_backend_role_not_forced_to_internship(predictor):
    result = predictor.predict(
        "Experienced Python backend engineer with FastAPI, PostgreSQL, REST APIs and production systems"
    )

    assert result["category"] == "backend"
    assert result["level"] in {"regular", "senior"}
