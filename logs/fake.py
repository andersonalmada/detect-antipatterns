from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import random

app = Flask(__name__)

SERVICES = [
    "payment-service",
    "checkout-service",
    "order-service",
    "inventory-service"
]

TRACE_IDS = [
    "aaa111", "bbb222", "ccc333"
]

MESSAGES = [
    "Checking payment processing loop iteration",
    "Payment validation complete",
    "Failed to update payment status",
    "Slow response from bank API",
    "Retrying payment authorization",
    "Order created successfully",
    "Payment request received",
    "Validating credit card information"
]

LEVELS = ["DEBUG", "INFO", "WARN", "ERROR"]
LEVEL_WEIGHTS = [0.60, 0.25, 0.10, 0.05]


def generate_logs(count: int):
    logs = []

    base_time = datetime.utcnow()

    for i in range(count):
        if i < 100:
            log_time = base_time + timedelta(milliseconds=i * 10)
        else:
            log_time = base_time + timedelta(seconds=i)

        log = {
            "timestamp": log_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "level": random.choices(LEVELS, weights=LEVEL_WEIGHTS, k=1)[0],
            "service": random.choice(SERVICES),
            "trace_id": random.choice(TRACE_IDS),
            "message": random.choice(MESSAGES)
        }

        logs.append(log)

    return logs

@app.route("/logs", methods=["GET"])
def get_logs():
    try:
        count = int(request.args.get("count", 1000))
        if count <= 0:
            count = 1

        logs = generate_logs(count)
        return jsonify(logs)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9092, debug=True)
