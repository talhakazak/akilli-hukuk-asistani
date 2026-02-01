from fastapi import FastAPI
import psycopg
from app.core.config import settings

import mlflow
import os
from datetime import datetime
import yaml

app = FastAPI(title=settings.APP_NAME)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("akilli-hukuk-asistani")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db/health")
def db_health():
    with psycopg.connect(settings.DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            result = cur.fetchone()[0]
    return {"db": "ok", "select": result}

def read_dvc_md5(dvc_file_path: str) -> str | None:
    # .dvc dosyası yaml formatında
    try:
        with open(dvc_file_path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        outs = doc.get("outs", [])
        if not outs:
            return None
        return outs[0].get("md5")
    except Exception:
        return None

@app.get("/mlflow/test-run")
def mlflow_test_run():
    dataset_dvc = "/app/data/raw/sample_case.txt.dvc"
    dataset_md5 = read_dvc_md5(dataset_dvc)

    with mlflow.start_run(run_name=f"smoke_{datetime.utcnow().isoformat()}"):
        mlflow.log_param("service", "api")
        mlflow.log_param("purpose", "smoke_test")
        if dataset_md5:
            mlflow.log_param("dataset_dvc_file", dataset_dvc)
            mlflow.log_param("dataset_md5", dataset_md5)
        mlflow.log_metric("ping", 1.0)
        run_id = mlflow.active_run().info.run_id

    return {"mlflow": "ok", "run_id": run_id, "tracking_uri": MLFLOW_TRACKING_URI, "dataset_md5": dataset_md5}
