from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def calculate_severity(value: int) -> str:
    if value <= 40:
        return "info"
    elif value <= 70:
        return "warning"
    else:
        return "critical"

HOSTS = [
    "app-server-01", "app-server-02", "backend-01", "backend-02",
    "cache-01", "db-01", "edge-01"
]

SERVICES = [
    "auth-service", "payment-service", "user-service", "inventory-service",
    "notification-service", "analytics-service"
]

def generate_alerts2(count: int):
    alerts = []

    # base: 3 horas atrás
    base_time = datetime.utcnow() - timedelta(hours=18)

    for _ in range(count):

        value = random.randint(1, 100)

        alert = {
            "name": f"TestAlert{random.randint(0, 9)}",
            "value": value,
            "severity": calculate_severity(value),
            "timestamp": (base_time + timedelta(
                hours=random.randint(0, 17),          # só dentro de 3h
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": random.choice(HOSTS),
            "service": random.choice(SERVICES)
        }

        alerts.append(alert)

    return alerts

def generate_alerts(count: int):
    alerts = []

    # base em uma semana
    base_time = datetime.utcnow() - timedelta(days=7)

    for _ in range(count):

        # gera valor aleatório
        value = random.randint(1, 100)

        alert = {
            "name": f"TestAlert{random.randint(0, 9)}",
            "value": value,
            "severity": calculate_severity(value),
            "timestamp": (base_time + timedelta(
                days=random.randint(0, 6),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": random.choice(HOSTS),
            "service": random.choice(SERVICES)
        }

        alerts.append(alert)

    return alerts


@app.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        count = int(request.args.get("count", 120))
        if count <= 0:
            count = 1

        alerts = generate_alerts2(count)
        return jsonify(alerts)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9091, debug=True)
