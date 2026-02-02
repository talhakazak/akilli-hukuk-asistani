# Akıllı Hukuk Asistanı

Bu repo, Akıllı Hukuk Asistanı projesinin local geliştirme altyapısını içerir.

LOCAL ÇALIŞTIRMA
1) Altyapıyı ayağa kaldır:
   cd infra
   docker compose up -d --build

SERVİSLER
- API (Swagger):        http://localhost:8000/docs
- MLflow UI:            http://localhost:5050
- MinIO Console:        http://localhost:9001
- MinIO S3 Endpoint:    http://localhost:9000
- PostgreSQL:           localhost:5432

SAĞLIK KONTROLLERİ
- curl http://localhost:8000/health
- curl http://localhost:8000/db/health
- curl http://localhost:8000/mlflow/test-run

DVC (DATA VERSION CONTROL)
- Default remote: s3store (MinIO bucket: akillidvc)

Komutlar:
- dvc pull
- dvc push

ALTYAPI BİLEŞENLERİ
- Docker & Docker Compose
- PostgreSQL
- FastAPI
- MLflow
- MinIO (S3 uyumlu)
- DVC
