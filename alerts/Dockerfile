# Use uma imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do backend para dentro do container
COPY . .

# Expõe a porta que o Flask vai usar
EXPOSE 5000

# Comando para rodar o app
CMD ["python", "app.py"]
