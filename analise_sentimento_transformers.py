from transformers import pipeline
import json

# Carrega o pipeline de sentimento com modelo multilíngue
analisador = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def analisar_sentimento(texto):
    resultado = analisador(texto[:512])[0]  # corta para 512 caracteres
    estrelas = int(resultado["label"][0])  # pega o número de estrelas da label, ex: '5 stars' -> 5
    if estrelas >= 4:
        return "positivo"
    elif estrelas == 3:
        return "neutro"
    else:
        return "negativo"

def classificar_reviews(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        dados = json.load(f)

    for review in dados:
        texto = review["review_text"]
        review["sentimento"] = analisar_sentimento(texto)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    print(f"[✓] {len(dados)} avaliações analisadas e salvas em {output_file}")

# Executa
if __name__ == "__main__":
    classificar_reviews("ml_reviews.json", "ml_reviews_com_sentimento.json")
