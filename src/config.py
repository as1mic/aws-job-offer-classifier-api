from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR / "raw" / "job_offers_hf_prepared.csv"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MODEL_DIR = PROJECT_ROOT / "model"

VECTORIZER_PATH = MODEL_DIR / "vectorizer.joblib"
CATEGORY_MODEL_PATH = MODEL_DIR / "category_model.joblib"
LEVEL_MODEL_PATH = MODEL_DIR / "level_model.joblib"
LABELS_PATH = MODEL_DIR / "labels.json"
METRICS_PATH = MODEL_DIR / "metrics.json"
