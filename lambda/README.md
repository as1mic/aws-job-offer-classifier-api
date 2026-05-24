# Lambda Deployment Notes

This folder contains a simple AWS Lambda handler for API Gateway proxy integration.

## Input

`event["body"]` should contain JSON like:

```json
{
  "text": "We are looking for a Junior Python Backend Developer with FastAPI, SQL and Docker."
}
```

## Output

The function returns a JSON body with:

- `category`
- `level`
- `confidence`
- `recommended`

## Packaging options

For the cheapest AWS Academy setup, include these files directly in the Lambda deployment package:

- `lambda/lambda_function.py`
- `src/`
- `model/`
- required dependencies from `lambda/requirements.txt`

Optional production-style approach:

- keep model artifacts in S3,
- download them during deployment or cold start,
- cache them in `/tmp`.

The first version intentionally avoids S3 model loading to keep the deployment easy and cheap.