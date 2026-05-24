from __future__ import annotations

import argparse
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


INPUT_PATH = PROJECT_ROOT / "data" / "raw" / "job_offers_hf.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "job_offers_hf_prepared.csv"
RANDOM_SEED = 42

CATEGORY_ORDER = ("backend", "frontend", "data", "devops", "other")
LEVEL_ORDER = ("internship", "junior", "regular", "senior")

PRIMARY_KEYWORD_CATEGORY_MAP = {
    "Python": "backend",
    "Java": "backend",
    ".NET": "backend",
    "Node.js": "backend",
    "PHP": "backend",
    "C++": "backend",
    "Golang": "backend",
    "Ruby": "backend",
    "Data Science": "data",
    "Data Engineer": "data",
    "SQL": "data",
    "DevOps": "devops",
    "Sysadmin": "devops",
    "Marketing": "other",
    "Sales": "other",
    "HR": "other",
    "Support": "other",
    "Project Manager": "other",
    "Product Manager": "other",
    "Business Analyst": "other",
    "Lead Generation": "other",
    "Design": "other",
    "Android": "other",
    "iOS": "other",
    "Unity": "other",
    "QA": "other",
    "QA Automation": "other",
}

BACKEND_HINTS = {
    "python",
    "django",
    "flask",
    "fastapi",
    "backend",
    "back-end",
    "api",
    "rest",
    "graphql",
    "node.js",
    "java",
    "spring",
    "php",
    "laravel",
    "ruby",
    "rails",
    "go",
    "golang",
    "postgresql",
    "mysql",
    "sqlalchemy",
    "microservices",
}
FRONTEND_HINTS = {
    "frontend",
    "front-end",
    "react",
    "vue",
    "angular",
    "javascript",
    "typescript",
    "html",
    "css",
    "next.js",
    "ui",
    "ux",
}
DATA_HINTS = {
    "data engineer",
    "data engineering",
    "data scientist",
    "data analyst",
    "machine learning",
    "ml",
    "ai",
    "llm",
    "rag",
    "etl",
    "elt",
    "airflow",
    "spark",
    "databricks",
    "analytics",
    "statistics",
    "numpy",
    "pandas",
    "big data",
    "clickhouse",
    "data pipeline",
}
DEVOPS_HINTS = {
    "devops",
    "site reliability",
    "sre",
    "cloud",
    "aws",
    "azure",
    "gcp",
    "docker",
    "kubernetes",
    "terraform",
    "ci/cd",
    "linux",
    "infrastructure",
    "monitoring",
    "prometheus",
    "grafana",
    "jenkins",
    "splunk",
    "serverless",
    "lambda",
}
OTHER_HINTS = {
    "marketing",
    "sales",
    "customer support",
    "recruiter",
    "hr",
    "operations",
    "business development",
    "project manager",
    "product manager",
}

LEVEL_KEYWORDS = {
    "internship": {"intern", "internship", "trainee", "student", "working student"},
    "junior": {"junior", "jr", "entry level", "entry-level", "graduate", "associate"},
    "regular": {"mid", "mid-level", "midlevel", "middle", "regular"},
    "senior": {"senior", "lead", "principal", "staff", "architect", "head of"},
}
EXP_YEARS_TO_LEVEL = {
    "no_exp": "internship",
    "1y": "junior",
    "2y": "junior",
    "3y": "regular",
    "5y": "senior",
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def count_hints(text: str, hints: set[str]) -> int:
    lowered = text.lower()
    return sum(1 for hint in hints if hint in lowered)


def score_categories(text: str) -> dict[str, int]:
    return {
        "backend": count_hints(text, BACKEND_HINTS),
        "frontend": count_hints(text, FRONTEND_HINTS),
        "data": count_hints(text, DATA_HINTS),
        "devops": count_hints(text, DEVOPS_HINTS),
        "other": count_hints(text, OTHER_HINTS),
    }


def infer_category(primary_keyword: str, title: str, description: str) -> str | None:
    text = f"{title} {description}".lower()
    primary_keyword = (primary_keyword or "").strip()

    if primary_keyword == "JavaScript":
        scores = score_categories(text)
        if scores["frontend"] >= scores["backend"]:
            return "frontend"
        return "backend"

    if primary_keyword in PRIMARY_KEYWORD_CATEGORY_MAP:
        mapped_category = PRIMARY_KEYWORD_CATEGORY_MAP[primary_keyword]
        if mapped_category != "other":
            return mapped_category

    scores = score_categories(text)
    best_category = max(scores, key=scores.get)
    if scores[best_category] >= 2:
        return best_category

    if primary_keyword in PRIMARY_KEYWORD_CATEGORY_MAP:
        return PRIMARY_KEYWORD_CATEGORY_MAP[primary_keyword]

    return None


def infer_level(exp_years: str, title: str, description: str) -> str:
    text = f"{title} {description}".lower()

    for level in ("internship", "senior", "junior", "regular"):
        if any(re.search(r"\b" + re.escape(keyword) + r"\b", text) for keyword in LEVEL_KEYWORDS[level]):
            return level

    return EXP_YEARS_TO_LEVEL.get((exp_years or "").strip(), "regular")


def prepare_dataset(
    input_path: Path = INPUT_PATH,
    output_path: Path = OUTPUT_PATH,
    per_category_limit: int = 5000,
    per_combo_cap: int = 1200,
) -> pd.DataFrame:
    dataframe = pd.read_csv(input_path)
    dataframe = dataframe[dataframe["Long Description_lang"] == "en"].copy()

    records = []
    for _, row in dataframe.iterrows():
        title = normalize_text(str(row.get("Position", "")))
        description = normalize_text(str(row.get("Long Description", "")))
        company = normalize_text(str(row.get("Company Name", "")))
        exp_years = str(row.get("Exp Years", ""))
        primary_keyword = str(row.get("Primary Keyword", ""))
        record_id = str(row.get("id", ""))

        text = normalize_text(f"{title} {description}")
        if len(text) < 120 or len(text) > 14000:
            continue

        category = infer_category(primary_keyword, title, description)
        if not category:
            continue

        level = infer_level(exp_years, title, description)
        records.append(
            {
                "text": text,
                "category": category,
                "level": level,
                "source": "hf_djinni",
                "title": title,
                "company": company,
                "url": "",
                "record_id": record_id,
                "primary_keyword": primary_keyword,
                "exp_years": exp_years,
            }
        )

    random.seed(RANDOM_SEED)
    random.shuffle(records)

    grouped_by_combo: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for record in records:
        grouped_by_combo[(record["category"], record["level"])].append(record)

    balanced_records = []
    category_counts: Counter[str] = Counter()

    for category in CATEGORY_ORDER:
        for level in LEVEL_ORDER:
            combo_records = grouped_by_combo.get((category, level), [])
            for record in combo_records[:per_combo_cap]:
                if category_counts[category] >= per_category_limit:
                    break
                balanced_records.append(record)
                category_counts[category] += 1

    prepared_df = pd.DataFrame(
        balanced_records,
        columns=[
            "text",
            "category",
            "level",
            "source",
            "title",
            "company",
            "url",
            "record_id",
            "primary_keyword",
            "exp_years",
        ],
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prepared_df.to_csv(output_path, index=False)

    print(f"Saved prepared HF dataset to {output_path}")
    print(f"Rows saved: {len(prepared_df)}")
    print("Category distribution:", prepared_df["category"].value_counts().to_dict())
    print("Level distribution:", prepared_df["level"].value_counts().to_dict())
    return prepared_df


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare the Hugging Face recruitment dataset for training.")
    parser.add_argument(
        "--input",
        default=str(INPUT_PATH),
        help="Path to the raw Hugging Face CSV file.",
    )
    parser.add_argument(
        "--output",
        default=str(OUTPUT_PATH),
        help="Path to the prepared training CSV file.",
    )
    parser.add_argument(
        "--per-category-limit",
        type=int,
        default=5000,
        help="Maximum rows per category in the prepared dataset.",
    )
    parser.add_argument(
        "--per-combo-cap",
        type=int,
        default=1200,
        help="Maximum rows per category/level combination.",
    )
    args = parser.parse_args()

    prepare_dataset(
        input_path=Path(args.input),
        output_path=Path(args.output),
        per_category_limit=args.per_category_limit,
        per_combo_cap=args.per_combo_cap,
    )


if __name__ == "__main__":
    main()
