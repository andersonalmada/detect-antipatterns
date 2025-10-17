from flask import Flask, jsonify
import time

app = Flask(__name__)

# Dados iniciais (exemplo de alertas)
alertas = [
    {
        "labels": {"alertname": "TestAlert", "id": "1", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T11:20:50Z",
        "value": "1"
    },
    {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T11:25:00Z",
        "value": "0.5"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T13:00:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T13:50:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T11:00:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert2", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert2", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert2", "id": "2", "severity": "warning"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert3", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },
    {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T11:25:00Z",
        "value": "0.5"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T13:00:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T13:50:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T11:00:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert2", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:50:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert2", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:50:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert2", "id": "2", "severity": "warning"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },
        {
        "labels": {"alertname": "TestAlert3", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    },{
        "labels": {"alertname": "TestAlert3", "id": "2", "severity": "critical"},
        "annotations": {"summary": "Alerta de teste 2", "description": "Somente teste"},
        "state": "pending",
        "activeAt": "2025-10-16T10:59:00Z",
        "value": "0.2"
    }  

]

@app.route('/api/v1/alerts', methods=['GET'])
def get_alertas():
    # Retorna sempre o mesmo JSON, mas você pode modificar antes de enviar
    return jsonify({"status": "success", "data": {"alerts": alertas}})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9091, debug=True)