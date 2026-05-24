import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.predictor import predict_job_offer


SAMPLE_TEXTS = [
    "We are looking for a Junior Python Backend Developer with FastAPI, SQL, Docker and REST API experience.",
    "Senior DevOps Engineer needed for AWS, Kubernetes, Terraform and CI/CD pipelines.",
    "Internship in data analysis with Python, pandas, SQL and Power BI.",
    "Regular Frontend Developer with React, TypeScript, HTML and responsive design skills.",
]


def main() -> None:
    for text in SAMPLE_TEXTS:
        result = predict_job_offer(text)
        print(f"Input: {text}")
        print(f"Prediction: {result}\n")


if __name__ == "__main__":
    main()