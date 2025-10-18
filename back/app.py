from flask import Flask, jsonify, request
import requests
from config import FIELD_MAP, EXTERNAL_API_URL, TS_INI, TS_FIM
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

app = Flask(__name__)

# Extract a value from a nested path, e.g., 'labels.alertname'
def extract_field(alert, path):
    parts = path.split(".")
    value = alert
    for part in parts:
        value = value.get(part, None) if isinstance(value, dict) else None
    return value

# Helper to add "exceeded" field
def add_exceeded_flag(item, count, limit):
    item["exceeded"] = count >= limit
    return item

def excesso_estatistico_grupo(items, k=2, limit=10):
    counts = [item["count"] for item in items]
    media = np.mean(counts)
    desvio = np.std(counts)
    limite_auto = media + k * desvio
    print(limite_auto)
    for item in items:
        item["exceeded"] = bool(item["count"] >= limite_auto or item["count"] >= limit)
    return items

def excesso_media(items, limit=10):
    counts = [item["count"] for item in items]
    media = np.mean(counts)
    print(media)
    for item in items:
        item["exceeded"] = bool(item["count"] >= media or item["count"] >= limit)
    return items

def excesso_isolation_forest_grupo(items, contamination=0.05, window_size=50, limit=10):
    if not items:
        return []

    # pega apenas os counts
    counts = [item["count"] for item in items]
    hist = counts[-window_size:]  # janela mais recente

    # fallback simples se todos os valores forem iguais
    if len(set(hist)) <= 1:
        limite_auto = max(hist)
        for item in items[-len(hist):]:
            item["exceeded"] = bool(item["count"] >= limite_auto or item["count"] >= limit)
        return items

    df_hist = pd.DataFrame({"alertas": hist})
    model = IsolationForest(contamination=contamination, random_state=42)

    try:
        df_hist["anomalia"] = model.fit_predict(df_hist[["alertas"]])
        df_hist["anomalia"] = df_hist["anomalia"].map({1: False, -1: True})

        # limite automático = maior valor considerado normal
        non_anom = df_hist.loc[~df_hist["anomalia"], "alertas"]
        limite_auto = non_anom.max() if not non_anom.empty else df_hist["alertas"].max()

        print(limite_auto)

        # aplica exceeded em cada item
        for item in items[-len(hist):]:
            item["exceeded"] = bool(item["count"] >= limite_auto or item["count"] >= limit)

        return items

    except Exception:
        # fallback simples caso IsolationForest falhe
        limite_auto = max(hist)
        print(limite_auto)
        for item in items[-len(hist):]:
            item["exceeded"] = bool(item["count"] >= limite_auto or item["count"] >= limit)
        return items

# Generic alert grouping function
def group_alerts(
    alerts, 
    fields_to_group=None,
    window_minutes=None,
    start_ts=None,
    end_ts=None,
    return_count_only=False,
    extra_fields=None,
    limit=10,
    mode="limit"
):
    if not alerts:
        return []

    extra_fields = extra_fields or ["host", "service"]

    if fields_to_group is None:
        fields_to_group = [k for k in alerts[0].keys() if k not in ["timestamp", "value"]]

    dt_start = datetime.fromisoformat(start_ts.replace("Z", "+00:00")) if start_ts else None
    dt_end = datetime.fromisoformat(end_ts.replace("Z", "+00:00")) if end_ts else None

    temp_group = defaultdict(list) if not return_count_only else defaultdict(int)

    if return_count_only and window_minutes:
        temp_group = defaultdict(list)

    alerts_sorted = sorted(alerts, key=lambda x: x["timestamp"])

    for alert in alerts_sorted:
        ts = datetime.fromisoformat(alert["timestamp"].replace("Z", "+00:00"))

        if dt_start and ts < dt_start:
            continue
        if dt_end and ts > dt_end:
            continue

        key = tuple((field, alert.get(field)) for field in fields_to_group)

        if window_minutes is None:
            if return_count_only:
                temp_group[key] += 1
            else:
                temp_group[key].append({"timestamp": ts, "value": alert.get("value")})
        else:
            inserted = False
            for group in temp_group[key]:
                min_ts = min(group["timestamps"])
                max_ts = max(group["timestamps"])
                if abs(ts - min_ts) <= timedelta(minutes=window_minutes) or abs(ts - max_ts) <= timedelta(minutes=window_minutes):
                    if return_count_only:
                        group["count"] += 1
                    else:
                        group["timestamps"].append(ts)
                        group["values"].append(alert.get("value"))
                    inserted = True
                    break
            if not inserted:
                if return_count_only:
                    temp_group[key].append({"count": 1, "timestamps": [ts]})
                else:
                    temp_group[key].append({"timestamps": [ts], "values": [alert.get("value")]})

    result = []        
    for key, groups in temp_group.items():        
        if window_minutes is None:
            if return_count_only:
                base = {**dict(key), "count": groups}

                if mode == "limit":
                    base = add_exceeded_flag(base, groups, limit)
            else:
                base = {
                    **dict(key),
                    "timestamps": [g["timestamp"] for g in groups],
                    "values": [g["value"] for g in groups]
                }
                count = len(groups)

                if mode == "limit":
                    base = add_exceeded_flag(base, count, limit)

            first_alert = groups[0] if not return_count_only else alerts_sorted[0]
            for ef in extra_fields:
                if ef not in base:
                    base[ef] = first_alert.get(ef)

            result.append(base)
        else:
            for group in groups:
                base_alert = dict(key)
                if return_count_only:
                    base_alert["count"] = group["count"]
                    count = group["count"]
                else:
                    base_alert["timestamps"] = [
                        ts.isoformat() + "Z" for ts in group["timestamps"]
                    ]
                    base_alert["values"] = group["values"]
                    count = len(group["timestamps"])

                if mode == "limit":
                    base_alert = add_exceeded_flag(base_alert, count, limit)

                first_alert = alerts_sorted[0]
                for ef in extra_fields:
                    if ef not in base_alert:
                        base_alert[ef] = first_alert.get(ef)

                result.append(base_alert)                

    return result

# Fetch and format alerts from external API
def fetch_formatted_alerts():
    response = requests.get(EXTERNAL_API_URL)
    response.raise_for_status()
    raw_alerts = response.json().get("data", {}).get("alerts", [])
    formatted = []
    for alert in raw_alerts:
        formatted.append({new_name: extract_field(alert, orig) for orig, new_name in FIELD_MAP.items()})
    return formatted

# Endpoints

@app.route("/alerts", methods=["GET"])
def get_alerts():
    try:
        alerts = fetch_formatted_alerts()
        total = len(alerts)
        mode = request.args.get("mode", "limit")
        limit = int(request.args.get("limit", 10))

        exceeded = False
        if total >= limit:
            exceeded = True
        
        return jsonify({
            "total_alerts": total,
            "exceeded": exceeded,
            "data": alerts
        })
    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "data": str(e)}), 500
    
@app.route("/alerts_group_window", methods=["GET"])
def get_alerts_group_window():
    alerts = fetch_formatted_alerts()
    window_minutes = int(request.args.get("window", 60))
    fields_str = request.args.get("fields")
    fields = [f.strip() for f in fields_str.split(",")] if fields_str else None
    count_only = request.args.get("count_only", "false").lower() == "true"
    limit = int(request.args.get("limit", 10))
    grouped = group_alerts(alerts, fields_to_group=fields, window_minutes=window_minutes, return_count_only=count_only,limit=limit)
    return jsonify(grouped)

@app.route("/alerts_group_range", methods=["GET"])
def get_alerts_group_range():
    alerts = fetch_formatted_alerts()
    fields_str = request.args.get("fields")
    fields = [f.strip() for f in fields_str.split(",")] if fields_str else None
    start_ts = request.args.get("start", TS_INI)
    end_ts = request.args.get("end", TS_FIM)
    count_only = request.args.get("count_only", "true").lower() == "true"
    limit = int(request.args.get("limit", 10))
    mode = request.args.get("mode", "limit")

    grouped = group_alerts(alerts, fields_to_group=fields, start_ts=start_ts, end_ts=end_ts, return_count_only=count_only,limit=limit,mode=mode)

    if mode == "media":
        grouped = excesso_media(grouped, limit=limit)
    elif mode == "stat":
        print("ok")
        grouped = excesso_estatistico_grupo(grouped, limit=limit)
    elif mode == "ml":
        grouped = excesso_isolation_forest_grupo(grouped, limit=limit)

    return jsonify(grouped)

if __name__ == "__main__":
    app.run(debug=True)
