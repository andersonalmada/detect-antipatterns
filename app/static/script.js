// Elementos
const fileInput = document.getElementById('jsonFile');
const btnValidate = document.getElementById('btnValidate');
const btnSaveDb = document.getElementById('btnSaveDb');
const btnInMemory = document.getElementById('btnInMemory');
const btnAnalyze = document.getElementById('btnAnalyze');
const btnClearAlerts = document.getElementById('btnClearAlerts');
const limitInput = document.getElementById('limitValue');
const reduction = document.getElementById('reduction');
const output = document.getElementById('output');
const messages = document.createElement('div'); // mensagens gerais
document.querySelector('.container').prepend(messages);

let parsedJson = null;

const now = new Date();
const start = new Date(now);
start.setDate(start.getDate() - 1);

const format = d => d.toISOString().slice(0, 16); // corta os segundos e o 'Z'
document.getElementById("startDate").value = format(start);
document.getElementById("endDate").value = format(now);

function showAlert(message, type='success', duration=3000) {
    const container = document.getElementById('alertContainer');
    
    // Criar alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;

    container.appendChild(alertDiv);

    // Remover após tempo definido
    setTimeout(() => {
        alertDiv.classList.remove('show');
        alertDiv.classList.add('hide');
        setTimeout(() => container.removeChild(alertDiv), 500); // para efeito fade out
    }, duration);
}

// Função para validar estrutura do JSON
function validateJSON(json) {
    if(!Array.isArray(json)) return false;
    for(const item of json){
        if(!('host' in item && 'name' in item && 'service' in item && 'severity' in item && 'timestamp' in item && 'value' in item)) return false;
    }
    return true;
}

// Botão Validar
btnValidate.addEventListener('click', () => {
    if(!fileInput.files[0]) { 
        showAlert('Select a JSON file first.', 'error'); 
        return; 
    }
    const reader = new FileReader();
    reader.onload = () => {
        try{
            const json = JSON.parse(reader.result);
            if(validateJSON(json)) {
                parsedJson = json;
                output.textContent = JSON.stringify(json, null, 2);
                showAlert('JSON is valid and loaded.');
            } else {
                showAlert('Invalid JSON: missing required fields.', 'error');
            }
        } catch(e) {
            showAlert('Error parsing JSON: ' + e.message, 'error');
        }
    };
    reader.readAsText(fileInput.files[0]);
});

// Função genérica para enviar JSON para API
function sendToAPI(save=true) {
    if(!parsedJson) { 
        showAlert('Load and validate a JSON file first.', 'error'); 
        return; 
    }
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/alerts?save=' + save, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.upload.onprogress = (event) => {
        if(event.lengthComputable){
            const percent = (event.loaded / event.total) * 100;
            // Barra de progresso opcional
        }
    };

    xhr.onload = () => {
        if(xhr.status === 200){
            const resp = JSON.parse(xhr.responseText);
            output.textContent = JSON.stringify(resp, null, 2);
            showAlert('Sent successfully!');
        } else {
            showAlert('Error sending: ' + xhr.status, 'error');
        }
    };

    xhr.onerror = () => {
        showAlert('Network error during sending.', 'error');
    };

    xhr.send(JSON.stringify(parsedJson));
}

// Botões de envio
btnSaveDb.addEventListener('click', () => sendToAPI(true));
btnInMemory.addEventListener('click', () => sendToAPI(false));

// Botão de análise
btnAnalyze.addEventListener('click', () => {
    const limit = parseInt(limitInput.value);
    if (isNaN(limit) || limit < 1) {
        showAlert('Limit must be a positive integer.', 'error');
        return;
    }

    // Detect mode
    const mode = document.querySelector('input[name="detectionMode"]:checked').value;
    const source = document.querySelector('input[name="dataSource"]:checked').value == 'database';

    // Get date values
    const start = document.getElementById('startDate').value;
    const end = document.getElementById('endDate').value;

    if (!start || !end) {
        showAlert('Please select both start and end dates.', 'error');
        return;
    }

    // Convert to ISO and force Z at the end
    const startISO = new Date(start).toISOString();
    const endISO = new Date(end).toISOString();

    const url = `/api/detect/window?mode=${mode}&limit=${limit}`;

    //const url = `/api/detect?start=${startISO}&end=${endISO}&fields=name&count_only=true&mode=${mode}&database=${source}`;

    fetch(url, { method: 'GET' })
        .then(res => res.json())
        .then(data => {
            output.textContent = JSON.stringify(data, null, 2);
            showAlert('Detection completed!');
            
            if (data.total_alerts && data.grouped_alerts) {
                const total = data.total_alerts;
                const grouped = data.grouped_alerts;
                const reductionLocal = total - grouped;
                const percent = ((reductionLocal / total) * 100).toFixed(2);

                const summary = `Total alerts: ${total}\nGrouped alerts: ${grouped}\nReduction: ${reductionLocal} (${percent}%)`;

                reduction.textContent = summary;
            }
        })
        .catch(err => {
            showAlert('Error during detection: ' + err.message, 'error');
        });
});

btnClearAlerts.addEventListener('click', () => {
    if (!confirm('Are you sure you want to delete all alerts?')) {
        return;
    }

    fetch('/api/alerts/clear', {
        method: 'DELETE'
    })
    .then(res => {
        if (res.ok) {
            showAlert('All alerts have been deleted.', 'success');
            output.textContent = ''; // limpa a visualização também
        } else {
            showAlert('Failed to delete alerts.', 'error');
        }
    })
    .catch(err => {
        showAlert('Error while deleting: ' + err.message, 'error');
    });
});