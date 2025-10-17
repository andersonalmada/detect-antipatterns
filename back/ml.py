import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# ---------- CONFIGURAÇÕES ----------
WINDOW_SIZE = 50        # Número de horas a considerar no histórico
CONTAMINATION = 0.1    # % de dados que o Isolation Forest considera anomalias
# -----------------------------------

# Simulando dados históricos iniciais (substituir pelo seu histórico real)
alertas_iniciais = [5, 6, 6, 7, 8, 5, 6, 5, 8, 9, 9, 7, 6, 5, 8, 6, 4, 5, 9, 11, 8, 7, 6, 5, 7]
df = pd.DataFrame({'alertas': alertas_iniciais})

def detectar_excesso(df):
    """Detecta anomalias usando Isolation Forest e calcula limite automático"""
    # Considera apenas a janela mais recente
    df_hist = df.tail(WINDOW_SIZE).copy()
    
    # Treinando Isolation Forest
    model = IsolationForest(contamination=CONTAMINATION, random_state=42)
    df_hist['anomalia'] = model.fit_predict(df_hist[['alertas']])
    df_hist['anomalia'] = df_hist['anomalia'].map({1: False, -1: True})
    
    # Limite automático baseado nos pontos normais
    limite_auto = df_hist.loc[~df_hist['anomalia'], 'alertas'].max()
    
    # Último valor de alerta
    ultimo_alerta = df_hist['alertas'].iloc[-1]
    excesso = ultimo_alerta >= limite_auto
    
    return excesso, limite_auto, df_hist

# ---------- EXEMPLO DE USO ----------
# Suponha que a cada hora você receba um novo número de alertas
novos_alertas = [6, 4, 7, 10, 12, 5, 8, 9]

for alerta in novos_alertas:
    # Adiciona o novo dado
    df = pd.concat([df, pd.DataFrame({'alertas':[alerta]})], ignore_index=True)
    
    # Detecta excesso
    excesso, limite, df_hist = detectar_excesso(df)
    
    print(f"Novo alerta: {alerta} | Limite automático: {limite} | Excesso? {excesso}")

# Opcional: ver histórico com anomalias
print("\nHistórico com anomalias detectadas:")
print(df_hist)
