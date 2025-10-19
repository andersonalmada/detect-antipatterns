from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

def gerar_alertas(qtd_alertnames=5, qtd_por_alertname=10, start_date="2025-10-16"):
    """
    Gera alertas de teste no formato do Prometheus Alertmanager.
    - qtd_alertnames: quantidade de alertnames diferentes
    - qtd_por_alertname: quantidade de alertas por alertname
    - start_date: data inicial em formato YYYY-MM-DD
    """
    alertas = []
    severities = ["critical", "warning", "info"]
    base_date = datetime.fromisoformat(start_date + "T00:00:00")

    for i in range(qtd_alertnames):
        alertname = f"TestAlert{i}"
        for j in range(qtd_por_alertname):
            # gera horário random dentro de dois dias
            delta = timedelta(days=random.randint(0, 1), 
                              hours=random.randint(0, 23), 
                              minutes=random.randint(0, 59),
                              seconds=random.randint(0, 59))
            activeAt = (base_date + delta).isoformat() + "Z"

            alert = {
                "labels": {"alertname": alertname, "id": str(j+1), "severity": random.choice(severities)},
                "annotations": {"summary": "Alerta de teste", "description": "Somente teste"},
                "state": "pending",
                "activeAt": activeAt,
                "value": str(random.randint(1, 20))
            }
            alertas.append(alert)
    return alertas

@app.route('/api/v1/alerts', methods=['GET'])
def get_alertas():
    alertas = gerar_alertas(qtd_alertnames=10, qtd_por_alertname=5)
    print(len(alertas))
    
    return jsonify({"status": "success", "data": {"alerts": alertas}})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9091, debug=True)