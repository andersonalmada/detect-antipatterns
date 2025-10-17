import os

# URL da API externa
#EXTERNAL_API_URL = 'http://host.docker.internal:9091/api/v1/alerts'
EXTERNAL_API_URL = 'http://localhost:9091/api/v1/alerts'

# Mapeamento dos campos originais para novos nomes
FIELD_MAP = {
    "activeAt": "timestamp",
    "labels.alertname": "name",
    "labels.severity": "severity",
    "value": "value",
    "labels.service": "service",
    "labels.host": "host"
}

TS_INI = "2025-10-16T10:00:00Z"
TS_FIM = "2025-10-16T14:00:00Z"

# PostgreSQL
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "alertsdb")

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False