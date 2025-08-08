import sqlite3
import json
from datetime import datetime

def save_to_db(json_file, db_path="prisma/dev.db"):
    with open(json_file, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    conn = sqlite3.connect(db_path)
    conn.text_factory = lambda b: b.decode('utf-8', 'ignore')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Review (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reviewText TEXT NOT NULL,
            source TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            createdAt TEXT NOT NULL
        )
    """)

    for review in reviews:
        try:
            # --- MODIFICAÇÃO AQUI ---
            # Formata a data ISO 8601 e adiciona o 'Z' para indicar UTC
            created_at_dt = datetime.now().isoformat(timespec='seconds')
            created_at_str = created_at_dt + 'Z'
            # ------------------------

            cursor.execute(
                """
                INSERT INTO Review (reviewText, source, sentiment, createdAt)
                VALUES (?, ?, ?, ?)
                """,
                (
                    review["review_text"],
                    review["source"],
                    review["sentimento"],
                    created_at_str,
                )
            )
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados: {e}")
            print(f"Dados que causaram o erro: {review}")
            conn.rollback()
            continue

    conn.commit()
    conn.close()
    print(f"[✓] {len(reviews)} avaliações salvas no banco de dados.")

if __name__ == "__main__":
    save_to_db("ml_reviews.json")