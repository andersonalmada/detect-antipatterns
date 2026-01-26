FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Copia dependências
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY app.py .

# Expõe porta da aplicação
EXPOSE 5001

# Comando de execução
CMD ["python", "app.py"]
