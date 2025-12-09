import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Dados
df = pd.DataFrame({
    "Time": [1, 2, 4, 8],
    "100":  [0.5, 0,   0,   0],
    "200":  [8.7, 0,   0,   0],
    "400":  [23.7, 6.2, 0,   0],
    "800":  [24,  24,  2.6, 0],
    "1000": [24,  24,  14.4, 0],
})

# Tons de cinza (da cor mais clara à mais escura)
grays = ["#eeeeee", "#cccccc", "#aaaaaa", "#888888", "#444444"]

# Padrões para distinguir visualmente
patterns = ["///", "\\\\", "xx", "++", ""]

plt.figure(figsize=(12, 7))

x = np.arange(len(df["Time"]))
largura = 0.15

colunas = ["100", "200", "400", "800", "1000"]

for i, col in enumerate(colunas):
    barras = plt.bar(
        x + (i - 2)*largura,
        df[col],
        width=largura,
        label=f"{col} alertas",
        color=grays[i],      # escala de cinza
        edgecolor="black",   # contorno para dar contraste
        hatch=patterns[i]    # padrão visual
    )
    
    # Adicionar valor na barra
    for barra in barras:
        altura = barra.get_height()
        if altura > 0:
            plt.text(
                barra.get_x() + barra.get_width()/2,
                altura + 0.5,
                f"{altura}",
                ha="center",
                va="bottom",
                fontsize=9
            )

plt.xlabel("Time")
plt.ylabel("Detectou")
plt.title("Detectados por Volume de Alertas (Escala de Cinza + Padrões)")
plt.xticks(x, df["Time"])
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.3)

plt.tight_layout()
plt.show()
