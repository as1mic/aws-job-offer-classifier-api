from __future__ import annotations

import json
import sys
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.predictor import predict_job_offer  # noqa: E402


def _response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    try:
        body = event.get("body")
        if body is None:
            return _response(400, {"error": "Missing request body."})

        if isinstance(body, str):
            payload = json.loads(body)
        elif isinstance(body, dict):
            payload = body
        else:
            return _response(400, {"error": "Invalid request body format."})

        text = str(payload.get("text", "")).strip()
        if not text:
            return _response(400, {"error": "Field 'text' must not be empty."})

        prediction = predict_job_offer(text)
        return _response(200, prediction)

    except json.JSONDecodeError:
        return _response(400, {"error": "Invalid JSON body."})
    except Exception as exc:  # pragma: no cover
        return _response(500, {"error": "Internal server error.", "details": str(exc)})