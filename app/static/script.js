const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const validateBtn = document.getElementById('validateBtn');
const resetBtn = document.getElementById('resetBtn');
const progressBar = document.getElementById('progressBar');
const preview = document.getElementById('preview');
const messages = document.getElementById('messages');

let parsedJson = null;

// Função para mostrar mensagens
function setMessage(msg, type='success') {
    messages.textContent = msg;
    messages.style.color = type === 'error' ? 'red' : 'green';
}

// Função para resetar interface
function reset() {
    fileInput.value = '';
    preview.textContent = '(Nenhum conteúdo carregado)';
    messages.textContent = '';
    progressBar.style.width = '0%';
    parsedJson = null;
}

// Função para validar estrutura do JSON
function validateJSON(json) {
    if(!Array.isArray(json)) return false;
    for(const item of json){
        if(!('host' in item && 'name' in item && 'service' in item && 'severity' in item && 'timestamp' in item && 'value' in item)) return false;
    }
    return true;
}

// Botão de validar e mostrar
validateBtn.addEventListener('click', () => {
    if(!fileInput.files[0]) { 
        setMessage('Selecione um arquivo JSON.', 'error'); 
        return; 
    }
    const reader = new FileReader();
    reader.onload = () => {
        try{
            const json = JSON.parse(reader.result);
            if(validateJSON(json)) {
                parsedJson = json;
                preview.textContent = JSON.stringify(json, null, 2);
                setMessage('JSON válido e carregado.');
            } else {
                setMessage('JSON inválido: faltam campos obrigatórios.', 'error');
            }
        } catch(e) {
            setMessage('Erro ao parsear JSON: ' + e.message, 'error');
        }
    };
    reader.readAsText(fileInput.files[0]);
});

// Botão de enviar para API com barra de progresso
uploadBtn.addEventListener('click', () => {
    if(!parsedJson) { 
        setMessage('Carregue e valide um JSON primeiro.', 'error'); 
        return; 
    }
    try {
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/api/alerts', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.upload.onprogress = (event) => {
            if(event.lengthComputable){
                const percent = (event.loaded / event.total) * 100;
                progressBar.style.width = percent + '%';
            }
        };

        xhr.onload = () => {
            if(xhr.status === 200){
                setMessage('Enviado com sucesso!');
                preview.textContent = JSON.stringify(JSON.parse(xhr.responseText), null, 2);
            } else {
                setMessage('Erro no envio: ' + xhr.status, 'error');
            }
        };

        xhr.onerror = () => {
            setMessage('Erro de rede ao enviar.', 'error');
        };

        xhr.send(JSON.stringify(parsedJson));
    } catch(e) {
        setMessage('Erro: ' + e.message, 'error');
    }
});

// Botão de reset
resetBtn.addEventListener('click', reset);
