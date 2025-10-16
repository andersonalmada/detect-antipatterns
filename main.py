# Instale as bibliotecas se ainda não tiver:
# pip install sentence-transformers scikit-learn numpy

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np

# 1️⃣ Lista de alertas de exemplo
alertas = [
    "CPU usage high on server A",
    "Server B CPU overloaded",
    "Memory usage critical on server C",
    "Disk space low on server A",
    "Database connection timeout on server D",
    "Memory consumption exceeds threshold on server C",
    "Server B running out of disk space",
    "Connection to database failed on server E",
]

# 2️⃣ Gerar embeddings usando Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(alertas)

# 3️⃣ Agrupamento com K-Means
# Sabemos que existem 4 tipos de alertas: CPU, Memória, Disco, Banco de dados
kmeans = KMeans(n_clusters=4, random_state=1)
labels = kmeans.fit_predict(embeddings)

# 4️⃣ Mostrar clusters
clusters = {}
for alerta, label in zip(alertas, labels):
    clusters.setdefault(label, []).append(alerta)

for label, group in clusters.items():
    print(f"\nCluster {label} ({len(group)} alertas):")
    for alerta in group:
        print(f" - {alerta}")
