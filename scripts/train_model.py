from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import (
    CATEGORY_MODEL_PATH,
    LABELS_PATH,
    LEVEL_MODEL_PATH,
    METRICS_PATH,
    RAW_DATA_PATH,
    VECTORIZER_PATH,
)
from src.preprocessing import clean_text


def build_metrics(y_true, y_pred) -> dict:
    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision_weighted": round(float(precision_score(y_true, y_pred, average="weighted", zero_division=0)), 4),
        "recall_weighted": round(float(recall_score(y_true, y_pred, average="weighted", zero_division=0)), 4),
        "f1_weighted": round(float(f1_score(y_true, y_pred, average="weighted", zero_division=0)), 4),
        "classification_report": report,
    }


def train_models(dataset_path: str | Path = RAW_DATA_PATH) -> dict:
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(
            "Dataset file was not found: "
            f"{dataset_path}\n"
            "The repository keeps data/raw/ empty before Git push.\n"
            "Recreate the dataset with:\n"
            "1. python scripts/download_hf_dataset.py\n"
            "2. python scripts/prepare_hf_training_dataset.py\n"
            "3. python scripts/train_model.py"
        )

    dataset = pd.read_csv(dataset_path)
    dataset["clean_text"] = dataset["text"].fillna("").map(clean_text)

    X_train, X_test, y_category_train, y_category_test, y_level_train, y_level_test = train_test_split(
        dataset["clean_text"],
        dataset["category"],
        dataset["level"],
        test_size=0.2,
        random_state=42,
        stratify=dataset[["category", "level"]],
    )

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    category_model = LogisticRegression(max_iter=1000, random_state=42)
    level_model = LogisticRegression(max_iter=1000, random_state=42)

    category_model.fit(X_train_vec, y_category_train)
    level_model.fit(X_train_vec, y_level_train)

    category_predictions = category_model.predict(X_test_vec)
    level_predictions = level_model.predict(X_test_vec)

    metrics = {
        "dataset": {
            "rows": int(len(dataset)),
            "train_rows": int(len(X_train)),
            "test_rows": int(len(X_test)),
        },
        "category_model": build_metrics(y_category_test, category_predictions),
        "level_model": build_metrics(y_level_test, level_predictions),
    }

    VECTORIZER_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    joblib.dump(category_model, CATEGORY_MODEL_PATH)
    joblib.dump(level_model, LEVEL_MODEL_PATH)

    labels = {
        "categories": sorted(dataset["category"].unique().tolist()),
        "levels": sorted(dataset["level"].unique().tolist()),
    }

    with LABELS_PATH.open("w", encoding="utf-8") as file:
        json.dump(labels, file, indent=2)

    with METRICS_PATH.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train job offer classification models.")
    parser.add_argument(
        "--data",
        default=str(RAW_DATA_PATH),
        help="Path to the CSV dataset file. Default: data/raw/job_offers_hf_prepared.csv",
    )
    args = parser.parse_args()

    metrics = train_models(dataset_path=args.data)
    print("Training finished.")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
