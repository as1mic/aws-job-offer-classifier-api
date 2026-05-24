# AWS Job Offer Classifier API

Educational AWS + Machine Learning project for classifying IT job offers with a lightweight REST-style prediction flow.

## Project goal

The API predicts:

- `category`: `backend`, `frontend`, `data`, `devops`, `other`
- `level`: `internship`, `junior`, `regular`, `senior`
- `confidence`
- `recommended` for a Junior Python Backend Developer profile

Example response:

```json
{
  "category": "backend",
  "level": "junior",
  "confidence": 0.72,
  "recommended": true
}
```

## Final dataset

The final version of the project uses one main dataset:

- `data/raw/job_offers_hf_prepared.csv`

This file is prepared from the Hugging Face dataset:

- `lang-uk/recruitment-dataset-job-descriptions-english`

The repository does not keep large raw CSV files in Git. Instead, the dataset is recreated locally with scripts.

## Architecture

- `S3` stores the prepared dataset and model artifacts
- `Glue` catalogs the CSV dataset
- `Athena` runs SQL analysis on the dataset in S3
- `SageMaker Notebook` handles ETL, exploration, training, and evaluation
- `FastAPI` provides a local web demo with a simple frontend form
- `Lambda` serves the prediction logic
- `API Gateway` exposes the `/predict` HTTP endpoint

## Local setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Build the final dataset

Download the raw Hugging Face dataset:

```bash
python scripts/download_hf_dataset.py
```

Prepare the training CSV used by the project:

```bash
python scripts/prepare_hf_training_dataset.py
```

This creates:

- `data/raw/job_offers_hf_prepared.csv`

## Train the model

```bash
python scripts/train_model.py
python scripts/evaluate_model.py
```

By default, training uses:

- `data/raw/job_offers_hf_prepared.csv`

Artifacts are saved into `model/`:

- `vectorizer.joblib`
- `category_model.joblib`
- `level_model.joblib`
- `labels.json`
- `metrics.json`

## Test prediction locally

```bash
python scripts/test_prediction.py
pytest tests -p no:cacheprovider
```

## Run the local web demo

Start a small FastAPI server with a browser-friendly form:

```bash
uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000`

Available local routes:

- `GET /` - demo page
- `POST /api/predict` - JSON prediction endpoint
- `GET /health` - healthcheck

## Deploy to AWS

Detailed deployment steps are in [docs/aws_deployment_steps.md](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/docs/aws_deployment_steps.md).

For Lambda packaging, build the final deployment zip on Linux, for example in AWS CloudShell, because `numpy`, `scipy`, and `scikit-learn` are compiled dependencies.

## University requirements checklist

- REST API endpoint: yes, via Lambda + API Gateway
- AWS services: S3, Glue, Athena, SageMaker Notebook, Lambda, API Gateway
- Git and remote repository: ready to initialize and push
- ETL/ELT or processing in SageMaker Notebook: included
- Big Data solution: large external recruitment dataset + S3 + Glue + Athena
- Machine Learning solution: TF-IDF + Logistic Regression + rule-based post-processing
- Analysis and evaluation of results: notebook, metrics, report

## Useful commands

```bash
python scripts/download_hf_dataset.py
python scripts/prepare_hf_training_dataset.py
python scripts/train_model.py
python scripts/evaluate_model.py
python scripts/test_prediction.py
uvicorn app.main:app --reload
pytest tests -p no:cacheprovider
```
