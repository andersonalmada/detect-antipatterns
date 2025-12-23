from flask import Flask, request, jsonify
from collections import defaultdict
from datetime import datetime, timezone
import re

app = Flask(__name__)

def parse_duration_to_seconds(duration_str):
    if not duration_str or duration_str.lower() == "unknown":
        return None

    # Remove timestamp entre parênteses
    duration_str = duration_str.split("(")[0].strip().lower()

    total_seconds = 0

    patterns = {
        "days": r"(\d+)\s*day",
        "hours": r"(\d+)\s*h",
        "minutes": r"(\d+)\s*m",
        "seconds": r"(\d+)\s*s",
    }

    if m := re.search(patterns["days"], duration_str):
        total_seconds += int(m.group(1)) * 86400

    if m := re.search(patterns["hours"], duration_str):
        total_seconds += int(m.group(1)) * 3600

    if m := re.search(patterns["minutes"], duration_str):
        total_seconds += int(m.group(1)) * 60

    if m := re.search(patterns["seconds"], duration_str):
        total_seconds += int(m.group(1))

    return total_seconds if total_seconds > 0 else None

def detect_alerts_by_duration(groups):
    for group in groups:
        flag = False
        for alert in group["alerts"]:

            # Só avalia duração para lembretes
            if alert.get("tipo_notificacao") != "Lembrete de Alerta":
                continue

            duration_seconds = parse_duration_to_seconds(alert.get("duracao"))

            if duration_seconds is None:
                continue
            if duration_seconds <= 900:  # 15 min
                alert["reason"] = "detect_unstable_alert"
                alert["excessive"] = True
                flag = True
            elif duration_seconds <= 7200:  # 2h
                alert["reason"] = "detect_short_persistent_alert"
                alert["excessive"] = True
                flag = True
            elif duration_seconds <= 86400:  # 24h
                alert["reason"] = "detect_persistent_alert"
                alert["excessive"] = True
                flag = True
            elif duration_seconds <= 604800:  # 7 dias
                alert["reason"] = "detect_long_persistent_alert"
                alert["excessive"] = True
                flag = True
            else:
                alert["reason"] = "detect_continuous_degradation"
                alert["excessive"] = True
                flag = True
        if flag == True:
            group["detected"] = True
            group["reason"] = "detect_alerts_duration"                

    return groups

def normalize_timestamp(date_str):
    """
    Converte:
    'Quarta, 17 de dezembro de 2025 15:31'
    para:
    '2025-12-17T15:31:00Z'
    """

    meses = {
        "janeiro": "01",
        "fevereiro": "02",
        "março": "03",
        "abril": "04",
        "maio": "05",
        "junho": "06",
        "julho": "07",
        "agosto": "08",
        "setembro": "09",
        "outubro": "10",
        "novembro": "11",
        "dezembro": "12",
    }

    # Remove o dia da semana (antes da vírgula)
    date_str = date_str.split(",", 1)[1].strip()

    # Ex: "17 de dezembro de 2025 15:31"
    partes = date_str.split()

    dia = partes[0]
    mes = meses[partes[2].lower()]
    ano = partes[4]
    hora = partes[5]

    iso = f"{ano}-{mes}-{dia}T{hora}:00"

    return datetime.fromisoformat(iso).replace(
        tzinfo=timezone.utc
    ).isoformat().replace("+00:00", "Z")

def group_alerts_by_hour(alerts):
    """
    Agrupa alertas por hora.
    Dentro de cada hora, os alertas permanecem disponíveis
    para subagrupamentos por host, service e name.
    """
    groups = defaultdict(list)

    for alert in alerts:
        ts = datetime.fromisoformat(alert["data_alerta"].replace("Z", "+00:00"))
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
    que compartilham o mesmo host, service e name,
    dentro do mesmo grupo horário.
    """
    for group in groups:
        subgroups = defaultdict(list)

        # Subagrupamento por host, service e name
        for alert in group["alerts"]:
            key = (alert["servidor"], alert["mensagem"])
            subgroups[key].append(alert)

        # Verificação de redundância temporal por subgrupo
        for (_, _), alerts in subgroups.items():
            alerts_sorted = sorted(
                alerts,
                key=lambda x: datetime.fromisoformat(x["data_alerta"].replace("Z", "+00:00"))
            )

            for i in range(1, len(alerts_sorted)):
                t1 = datetime.fromisoformat(alerts_sorted[i - 1]["data_alerta"].replace("Z", "+00:00"))
                t2 = datetime.fromisoformat(alerts_sorted[i]["data_alerta"].replace("Z", "+00:00"))

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
        alert["data_alerta"] = normalize_timestamp(alert.pop("data_alerta"))
        alert["excessive"] = False
        alert["reason"] = ""
        
        
    grouped = group_alerts_by_hour(alerts)
    grouped = detect_alerts_by_duration(grouped)
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
    app.run(host="0.0.0.0", port=5002, debug=True)
