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
    "app-server-01", "app-server-02"
]

SERVICES = [
    "auth-service", "payment-service", "user-service", "inventory-service",
    "notification-service", "analytics-service"
]

# -------------------------------
# NEW: Generate alerts over 24h
# -------------------------------
def generate_alerts_24h(count: int):
    alerts = []

    # base time = start of day (00:00 UTC)
    now = datetime.utcnow()
    base_time = now.replace(hour=0, minute=0, second=0, microsecond=0)

    for _ in range(count):
        value = random.randint(1, 100)

        alert_time = base_time + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        alert = {
            "name": f"TestAlert{random.randint(0, 9)}",
            "value": value,
            "severity": calculate_severity(value),
            "timestamp": alert_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": random.choice(HOSTS),
            "service": random.choice(SERVICES)
        }

        alerts.append(alert)

    return alerts


# your old generators kept for compatibility
def generate_alerts2(count: int):
    alerts = []

    # FIXED hour: current hour only (e.g. 17:00 → 17:59)
    now = datetime.utcnow()
    base_time = now.replace(minute=0, second=0, microsecond=0)

    for _ in range(count):
        value = random.randint(1, 100)

        alert_time = base_time + timedelta(
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        alert = {
            "name": f"TestAlert{random.randint(0, 9)}",
            "value": value,
            "severity": calculate_severity(value),
            "timestamp": alert_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": random.choice(HOSTS),
            "service": random.choice(SERVICES)
        }

        alerts.append(alert)

    return alerts

# your old generators kept for compatibility
def generate_alerts_real(count: int):
    alerts = []

    # FIXED hour: current hour only (e.g. 17:00 → 17:59)
    now = datetime.utcnow()

    for _ in range(count):
        value = random.randint(1, 100)

        alert = {
            "name": f"TestAlert{random.randint(0, 9)}",
            "value": value,
            "severity": calculate_severity(value),
            "timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": random.choice(HOSTS),
            "service": random.choice(SERVICES)
        }

        alerts.append(alert)

    return alerts

def generate_alerts(count: int, days=7, hours=24):
    alerts = []
    base_time = datetime.utcnow() - timedelta(days=days)

    for _ in range(count):
        value = random.randint(1, 100)

        alert_time = base_time + timedelta(
            days=random.randint(0, days-1),
            hours=random.randint(0, hours-1),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        alert = {
            "name": f"TestAlert{random.randint(0, 9)}",
            "value": value,
            "severity": calculate_severity(value),
            "timestamp": alert_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "host": random.choice(HOSTS),
            "service": random.choice(SERVICES)
        }

        alerts.append(alert)

    return alerts


@app.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        count = int(request.args.get("count", 1000))
        if count <= 0:
            count = 1

        mode = request.args.get("mode", "24h")

        if mode == "24h":
            alerts = generate_alerts_24h(count)
        elif mode == "1h":
            alerts = generate_alerts2(count)
        elif mode == "real":
            alerts = generate_alerts_real(count)
        else:
            alerts = generate_alerts(count)

        return jsonify(alerts)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9091, debug=True)
