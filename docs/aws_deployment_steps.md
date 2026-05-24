# AWS Deployment Steps

This guide is written for **AWS Academy Learner Lab**, so the architecture stays simple and low cost.

## Important warnings

- Do not click **Reset Lab** unless your teacher explicitly asks for it.
- Stop the **SageMaker Notebook Instance** after work to avoid unnecessary resource usage.
- Avoid expensive services such as **RDS**, **Redshift**, and **NAT Gateway**.
- Keep everything in one AWS region during the project.

## 1. Start Learner Lab

1. Open AWS Academy and start the Learner Lab.
2. Wait until the AWS Console button becomes active.
3. Open the AWS Console and confirm the selected region.

## 2. Prepare the dataset locally

1. Download the raw Hugging Face dataset:

```bash
python scripts/download_hf_dataset.py
```

2. Prepare the final training dataset:

```bash
python scripts/prepare_hf_training_dataset.py
```

3. The final CSV used by the project is:
   - `data/raw/job_offers_hf_prepared.csv`

## 3. Create an S3 bucket

1. Go to **Amazon S3**.
2. Create a bucket with a unique name, for example `aws-job-offer-classifier-<yourname>`.
3. Inside the bucket create these folders:
   - `raw/`
   - `processed/`
   - `model/`
   - `athena-results/`
4. Upload `data/raw/job_offers_hf_prepared.csv`.
5. The expected S3 path is:
   - `s3://your-bucket-name/raw/job_offers_hf_prepared.csv`

## 4. Prepare Glue metadata

1. Open **AWS Glue**.
2. Create a database named `job_offer_db`.
3. Create a **Glue Crawler**.
4. As the data source, select the S3 path `s3://your-bucket-name/raw/`.
5. Choose the previously created database `job_offer_db`.
6. Run the crawler.
7. Confirm that the table for the CSV file appears in Glue Data Catalog.

## 5. Query the dataset in Athena

1. Open **Amazon Athena**.
2. Set the query result location to `s3://your-bucket-name/athena-results/`.
3. Open the database `job_offer_db`.
4. Run the SQL examples from [docs/athena_queries.sql](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/docs/athena_queries.sql).
5. Save screenshots of successful queries for the final presentation.

## 6. Create SageMaker Notebook

1. Open **Amazon SageMaker AI** or **SageMaker Notebook Instances**, depending on the lab interface.
2. Create a notebook instance with the smallest available instance type.
3. Wait until the notebook becomes available.
4. Open Jupyter or JupyterLab.
5. Upload the repository ZIP file or clone the Git repository.
6. Open [notebooks/training_notebook.ipynb](/c:/Users/Asim/Desktop/aws-job-offer-classifier-api/notebooks/training_notebook.ipynb).
7. Run the notebook step by step.

## 7. Train and save the model

1. Load the prepared Hugging Face CSV from local project path or from S3.
2. Run preprocessing and model training cells.
3. Save these artifacts:
   - `vectorizer.joblib`
   - `category_model.joblib`
   - `level_model.joblib`
   - `labels.json`
   - `metrics.json`
4. Upload the saved model files to `s3://your-bucket-name/model/` if you want a backup.

## 8. Create Lambda function

1. Open **AWS Lambda**.
2. Create a new function named `job-offer-classifier-lambda`.
3. Choose Python 3.10+ runtime.
4. Package the deployment with:
   - `lambda/lambda_function.py`
   - `src/`
   - `model/`
   - dependencies from `lambda/requirements.txt`
5. Upload the ZIP package or use a Lambda layer for dependencies.

## 9. Create API Gateway HTTP API

1. Open **Amazon API Gateway**.
2. Create an **HTTP API**.
3. Add a Lambda integration pointing to `job-offer-classifier-lambda`.
4. Create route:
   - `POST /predict`
5. Deploy the API.
6. Copy the invoke URL.

## 10. Test the endpoint

Use `curl`:

```bash
curl -X POST "https://your-api-id.execute-api.region.amazonaws.com/predict" ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"We are looking for a Junior Python Backend Developer with FastAPI, SQL, Docker and REST API experience.\"}"
```

## 11. Collect presentation evidence

Take screenshots of:

- S3 bucket and folders
- Glue database and crawler result
- Athena query output
- SageMaker notebook execution
- Lambda test result
- API Gateway route
- Postman or curl response
