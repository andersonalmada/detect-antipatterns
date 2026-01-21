from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime, timedelta
import json

app = Flask(__name__)

def split_by_time_window(alerts, window_minutes=10):
    if not alerts:
        return []

    alerts = sorted(
        alerts,
        key=lambda a: datetime.fromisoformat(a["timestamp"].replace("Z", "+00:00"))
    )

    groups = []
    current_group = [alerts[0]]

    for prev, curr in zip(alerts, alerts[1:]):
        t_prev = datetime.fromisoformat(prev["timestamp"].replace("Z", "+00:00"))
        t_curr = datetime.fromisoformat(curr["timestamp"].replace("Z", "+00:00"))

        if t_curr - t_prev <= timedelta(minutes=window_minutes):
            current_group.append(curr)
        else:
            groups.append(current_group)
            current_group = [curr]

    groups.append(current_group)
    return groups

def group_by_hour_host_name_service_severity(alerts, window_minutes=10):
    # hour -> host -> name -> service -> severity -> list(alerts)
    groups = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list)))))

    for alert in alerts:
        ts = datetime.fromisoformat(alert["timestamp"].replace("Z", "+00:00"))
        hour_key = ts.replace(minute=0, second=0, microsecond=0)

        groups[hour_key][alert["host"]][alert["name"]][alert["service"]][alert["severity"]].append(alert)

    result = []

    for hour, hosts in sorted(groups.items()):
        hour_block = {
            "hour": hour.isoformat() + "Z",
            "groups": []
        }

        for host, names in hosts.items():
            for name, services in names.items():
                for service, severities in services.items():
                    for severity, items in severities.items():

                        # quebra em janelas de tempo
                        time_groups = split_by_time_window(items, window_minutes=window_minutes)

                        for tg in time_groups:
                            slim_alerts = [
                                {
                                    "timestamp": item["timestamp"],
                                    "value": item["value"],
                                }
                                for item in tg
                            ]

                            hour_block["groups"].append({
                                "host": host,
                                "name": name,
                                "service": service,
                                "severity": severity,
                                "count": len(tg),
                                "alerts": slim_alerts
                            })

        result.append(hour_block)

    return result

@app.post("/detector")
def detector():
    #alerts = request.get_json()
    alerts = json.load(request.files["file"])
    window_minutes = int(request.args.get("window", 10))
    print(len(json.dumps(alerts).encode("utf-8")))

    grouped = group_by_hour_host_name_service_severity(alerts, window_minutes)
    
    print(len(json.dumps(grouped).encode("utf-8")))
    
    total_groups = sum(len(hour["groups"]) for hour in grouped)
    
    response = {
        "analyzed": len(alerts),
        "detected": total_groups,
        #"data": grouped
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
