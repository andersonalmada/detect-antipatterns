from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime
import numpy as np
import requests

app = Flask(__name__)

#Limit-based
def limit_excess(items, limit=10, team=1):
    for item in items:
        item["detected"] = item["count"] >= limit * team
    return items

#Mean-based
def mean_excess(items, team=1):
    counts = [item["count"] for item in items]
    avg = np.mean(counts)
    for item in items:
        item["detected"] = bool(item["count"] >= avg * team)
    return items

#Z-Score
def statistical_excess_group(items, k=2):
    counts = [item["count"] for item in items]
    mean = np.mean(counts)
    std_dev = np.std(counts)
    auto_threshold = mean + k * std_dev    
    for item in items:
        item["detected"] = bool(item["count"] >= auto_threshold)
    return items

#EWMA
def ewma_excess(items, alpha=0.3, k=3, min_history=5):
    if not items:
        return items

    counts = [item["count"] for item in items]

    # Initialization with the first value
    ewma = counts[0]
    ewma_var = 0  # EWMA variance

    for i, item in enumerate(items):

        count = item["count"]

        if i == 0:
            # First point: anomaly detection is disabled
            item["detected"] = False
            continue

        # === Update EWMA ===
        previous_ewma = ewma
        ewma = alpha * count + (1 - alpha) * previous_ewma

        # === Update EWMA variance ===
        ewma_var = (1 - alpha) * (ewma_var + alpha * (count - previous_ewma) ** 2)

        # === Dynamic threshold ===
        threshold = ewma + k * (ewma_var ** 0.5)
        
        if i < min_history:
            # Not enough historical data yet
            item["detected"] = False
        else:
            item["detected"] = count >= threshold

    return items

def group_alerts_by_hour(alerts):
    groups = defaultdict(list)

    for alert in alerts:
        ts = datetime.fromisoformat(alert["timestamp"].replace("Z", "+00:00"))
        hour_key = ts.replace(minute=0, second=0, microsecond=0)
        groups[hour_key].append(alert)

    result = []
    for hour, items in sorted(groups.items()):
        result.append({
            "count": len(items),
            "alerts": items
        })

    return result

def group_by_hour_name_service(alerts):
    # Estrutura:
    # groups[hour][host][name][service] = [alerts...]
    groups = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))

    for alert in alerts:
        ts = datetime.fromisoformat(alert["timestamp"].replace("Z", "+00:00"))
        hour_key = ts.replace(minute=0, second=0, microsecond=0)

        name = alert["name"]
        service = alert["service"]
        host = alert["host"]

        groups[hour_key][host][name][service].append(alert)

    result = []

    for hour, hosts in sorted(groups.items()):
        hour_block = {
            "hour": hour.isoformat() + "Z",
            "groups": []
        }

        for host, names in hosts.items():
            for name, services in names.items():
                for service, items in services.items():
                    slim_alerts = [
                        {
                            "timestamp": item["timestamp"],
                            "value": item["value"]
                        }
                        for item in items
                    ]

                    hour_block["groups"].append({
                        "host": host,
                        "name": name,
                        "service": service,
                        "count": len(items),
                        #"alerts": slim_alerts
                    })

        result.append(hour_block)

    return result

@app.post("/detector")
def detect():
    #alerts = request.get_json()
    result = []
    count = request.args.get("count", "100")
    for i in range(30):        
        alerts = requests.get(f"http://localhost:9091/alerts?count={count}&mode=24h").json()
        grouped = group_alerts_by_hour(alerts)
        mode = request.args.get("mode", "limit")
        limit = int(request.args.get("limit", 10))
        team = int(request.args.get("team", 1))
        
        if mode == "limit":
            grouped = limit_excess(grouped, limit=limit, team=team)
        elif mode == "mean":
            grouped = mean_excess(grouped, team=team)
        elif mode == "zscore":
            grouped = statistical_excess_group(grouped)
        elif mode == "ewma":
            grouped = ewma_excess(grouped, alpha=0.2, k=1)                        
            
        detected = sum(1 for x in grouped if x["detected"])
        
        response = {
            "analyzed": len(grouped),
            "detected": detected,
            #"data": grouped
        }
        
        result.append(response)

    return jsonify(result)

@app.post("/solution")
def solution():
    alerts = request.get_json()
    grouped = group_by_hour_name_service(alerts)
    
    total_groups = sum(len(hour_block["groups"]) for hour_block in grouped)
    
    response = {
        "analyzed": len(alerts),
        "detected": total_groups,
        "data": grouped
    }

    return jsonify(response)

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5001)
