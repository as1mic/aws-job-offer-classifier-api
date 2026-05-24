from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import METRICS_PATH, RAW_DATA_PATH
from src.preprocessing import clean_text


def evaluate(dataset_path: str | Path = RAW_DATA_PATH) -> dict:
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
        "category_model": {
            "classification_report": classification_report(
                y_category_test, category_predictions, output_dict=True, zero_division=0
            ),
            "confusion_matrix_labels": sorted(y_category_test.unique().tolist()),
            "confusion_matrix": confusion_matrix(
                y_category_test,
                category_predictions,
                labels=sorted(y_category_test.unique().tolist()),
            ).tolist(),
        },
        "level_model": {
            "classification_report": classification_report(
                y_level_test, level_predictions, output_dict=True, zero_division=0
            ),
            "confusion_matrix_labels": sorted(y_level_test.unique().tolist()),
            "confusion_matrix": confusion_matrix(
                y_level_test,
                level_predictions,
                labels=sorted(y_level_test.unique().tolist()),
            ).tolist(),
        },
    }

    with Path(METRICS_PATH).open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)

    return metrics


def main() -> None:
    metrics = evaluate()
    print("Evaluation results")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()