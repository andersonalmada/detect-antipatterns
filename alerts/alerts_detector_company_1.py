from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime, timezone

app = Flask(__name__)

def normalize_timestamp(date_str):
    try:
        dt = datetime.strptime(date_str, "%m/%d/%Y %I:%M %p")
    except ValueError:
        dt = datetime.strptime(date_str, "%d/%m/%Y %I:%M %p")

    return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def group_alerts_by_hour(alerts):
    """
    Agrupa alertas por hora.
    Dentro de cada hora, os alertas permanecem disponíveis
    para subagrupamentos por host, service e name.
    """
    groups = defaultdict(list)

    for alert in alerts:
        ts = datetime.fromisoformat(alert["date"].replace("Z", "+00:00"))
        hour_key = ts.replace(minute=0, second=0, microsecond=0)
        groups[hour_key].append(alert)

    result = []
    for hour, items in sorted(groups.items()):
        result.append({
            "hour": hour.isoformat() + "Z",
            "count": len(items),
            "detected": False,
            "reason": "",
            "alerts": items
        })

    return result


def detect_time_window(groups, window_seconds=60):
    """
    Detecta redundância temporal apenas entre alertas
    que compartilham o mesmo title dentro do mesmo grupo horário.
    """
    for group in groups:
        subgroups = defaultdict(list)

        # Subagrupamento por host, service e name
        for alert in group["alerts"]:
            key = (alert["title"],alert["description"])
            subgroups[key].append(alert)

        # Verificação de redundância temporal por subgrupo
        for (_, _), alerts in subgroups.items():
            alerts_sorted = sorted(
                alerts,
                key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "+00:00"))
            )

            for i in range(1, len(alerts_sorted)):
                t1 = datetime.fromisoformat(alerts_sorted[i - 1]["date"].replace("Z", "+00:00"))
                t2 = datetime.fromisoformat(alerts_sorted[i]["date"].replace("Z", "+00:00"))

                if (t2 - t1).total_seconds() <= window_seconds:
                    alerts_sorted[i - 1]["excessive"] = alerts_sorted[i]["excessive"] = True                    
                    group["detected"] = True
                    group["reason"] = "detect_redundancy"
                    break

            if group["detected"]:
                break

    return groups


def detect_limit_excess(groups, limit=10, team=1):
    """
    Detecta excesso de alertas considerando o volume total
    por grupo horário.
    """
    for group in groups:
        if group["count"] >= limit * team and not group["detected"]:
            for alert in group["alerts"]:
                alert["excessive"] = True
                
            group["detected"] = True
            group["reason"] = "detect_limit_excess"

    return groups


@app.post("/detector")
def detector():
    alerts = request.get_json()
    limit = int(request.args.get("limit", 10))
    team = int(request.args.get("team", 1))
    
    for alert in alerts:
        alert["date"] = normalize_timestamp(alert["date"])
        alert["excessive"] = False
    
    grouped = group_alerts_by_hour(alerts)
    grouped = detect_limit_excess(grouped, limit=limit, team=team)
    grouped = detect_time_window(grouped)
    
    #total_detected = sum(1 for group in grouped if group["detected"])
    
    total_excessive = sum(
        1
        for group in grouped
        for alert in group["alerts"]
        if alert.get("excessive") is True
    )

    response = {
        "analyzed": len(alerts),
        "detected": total_excessive,
        "data": grouped
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
