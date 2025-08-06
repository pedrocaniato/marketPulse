import sqlite3
import json
from datetime import datetime

def save_to_db(json_file, db_path="prisma/dev.db"):
    with open(json_file, "r", encoding="utf-8") as f:
        reviews = json.load(f)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for review in reviews:
        cursor.execute(
            """
            INSERT INTO Review (reviewText, source, sentiment, createdAt)
            VALUES (?, ?, ?, ?)
            """,
            (
                review["review_text"],
                review["source"],
                review["sentimento"],
                datetime.now().isoformat(),
            )
        )

    conn.commit()
    conn.close()
    print(f"[✓] {len(reviews)} avaliações salvas no banco de dados.")

# Executar
if __name__ == "__main__":
    save_to_db("ml_reviews.json")
