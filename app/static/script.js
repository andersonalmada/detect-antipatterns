// Elementos
const fileInput = document.getElementById('jsonFile');
const btnValidate = document.getElementById('btnValidate');
const btnSaveDb = document.getElementById('btnSaveDb');
const btnInMemory = document.getElementById('btnInMemory');
const btnAnalyze = document.getElementById('btnAnalyze');
const limitInput = document.getElementById('limitValue');
const output = document.getElementById('output');
const messages = document.createElement('div'); // mensagens gerais
document.querySelector('.container').prepend(messages);

let parsedJson = null;

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
    if(isNaN(limit) || limit < 1){
        showAlert('Limit must be a positive integer.', 'error');
        return;
    }

    // Detect mode
    const mode = document.querySelector('input[name="detectionMode"]:checked').value;
    const source = document.querySelector('input[name="dataSource"]:checked').value == 'database';

    fetch('/api/detect?start=2025-10-16T10:00:00Z&end=2025-10-18T13:55:00Z&fields=name&count_only=true&mode='+mode+'&database='+source, {
        method: 'GET'
    })
    .then(res => res.json())
    .then(data => {
        output.textContent = JSON.stringify(data, null, 2);
        showAlert('Detection completed!');
    })
    .catch(err => {
        showAlert('Error during detection: ' + err.message, 'error');
    });
});
