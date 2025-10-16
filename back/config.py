# URL da API externa
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