from fastapi import FastAPI
import psycopg
from app.core.config import settings

import mlflow
import os
from datetime import datetime

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

@app.get("/mlflow/test-run")
def mlflow_test_run():
    # Basit bir run loglayıp run_id döndürüyoruz
    with mlflow.start_run(run_name=f"smoke_{datetime.utcnow().isoformat()}"):
        mlflow.log_param("service", "api")
        mlflow.log_param("purpose", "smoke_test")
        mlflow.log_metric("ping", 1.0)
        run_id = mlflow.active_run().info.run_id
    return {"mlflow": "ok", "run_id": run_id, "tracking_uri": MLFLOW_TRACKING_URI}
