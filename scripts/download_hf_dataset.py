from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


DATASET_NAME = "lang-uk/recruitment-dataset-job-descriptions-english"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw" / "job_offers_hf.csv"


def download_dataset(output_path: Path = DEFAULT_OUTPUT, limit: int | None = None) -> Path:
    try:
        from datasets import load_dataset
    except ImportError as exc:  # pragma: no cover
        raise SystemExit(
            "Missing dependency: install the 'datasets' package first, for example:\n"
            "python -m pip install datasets pyarrow"
        ) from exc

    dataset = load_dataset(DATASET_NAME, split="train")
    if limit:
        dataset = dataset.select(range(min(limit, len(dataset))))

    dataframe = dataset.to_pandas()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)

    print(f"Saved Hugging Face dataset to {output_path}")
    print(f"Rows saved: {len(dataframe)}")
    print(f"Columns: {list(dataframe.columns)}")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the Hugging Face English recruitment dataset.")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to the output CSV file. Default: data/raw/job_offers_hf.csv",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional row limit for a smaller local sample.",
    )
    args = parser.parse_args()

    download_dataset(output_path=Path(args.output), limit=args.limit)


if __name__ == "__main__":
    main()
