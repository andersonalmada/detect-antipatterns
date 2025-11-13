from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

SEVERITIES = ["info", "warning", "critical"]

def generate_alerts(count: int):
    alerts = []
    base_time = datetime(2025, 10, 16, 0, 0, 0)
    
    for i in range(count):
        alert = {
            "host": None,
            "name": f"TestAlert{random.randint(0, 9)}",  # variação de nome
            "service": None,
            "severity": random.choice(SEVERITIES),
            "timestamp": (base_time + timedelta(
                days=random.randint(0, 1),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "value": str(random.randint(1, 20))
        }
        alerts.append(alert)
    
    return alerts


@app.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        count = int(request.args.get("count", 100))  # número de objetos (default=10)
        if count <= 0:
            count = 1
        alerts = generate_alerts(count)
        return jsonify(alerts)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9091, debug=True)
