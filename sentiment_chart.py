import json
import matplotlib.pyplot as plt
from collections import Counter

# Carrega as avaliações do arquivo JSON
with open("ml_reviews.json", "r", encoding="utf-8") as f:
    reviews = json.load(f)

# Conta os sentimentos
sentimentos = [review["sentimento"] for review in reviews]
contagem = Counter(sentimentos)

# Dados para os gráficos
labels = contagem.keys()
valores = contagem.values()
cores = ["#2ecc71", "#f1c40f", "#e74c3c"]  # verde, amarelo, vermelho

# Gráfico de pizza
plt.figure(figsize=(6, 6))
plt.pie(valores, labels=labels, autopct="%1.1f%%", colors=cores, startangle=140)
plt.title("Distribuição dos Sentimentos das Avaliações")
plt.axis("equal")
plt.show()

# Gráfico de barras
plt.figure(figsize=(8, 5))
plt.bar(labels, valores, color=cores)
plt.title("Contagem de Sentimentos")
plt.xlabel("Sentimento")
plt.ylabel("Quantidade")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.show()
