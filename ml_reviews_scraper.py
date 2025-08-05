from playwright.sync_api import sync_playwright
import json

def scrape_reviews(product_url, max_reviews=25):
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(product_url, timeout=60000)

        # Clica no botão para abrir o modal
        print("[→] Procurando botão 'Mostrar todas as opiniões'...")
        show_more_btn = page.locator('button.show-more-click')
        show_more_btn.click()
        print("[✓] Botão clicado, aguardando modal...")

        # Aguarda o modal com artigos aparecer
        page.wait_for_selector('article[data-testid="comment-component"]', timeout=15000)

        # Localiza o contêiner do modal
        modal_container = page.locator('div[role="dialog"]')
        if not modal_container:
            print("[✘] Modal não encontrado.")
            return

        print("[→] Scrollando dentro do modal...")
        prev_count = 0
        attempts = 0

        # Loop até pegar o máximo ou não carregar mais nada
        while True:
            # Conta quantos artigos carregaram até agora
            articles = modal_container.locator('article[data-testid="comment-component"]')
            count = articles.count()

            print(f"[...] {count} avaliações carregadas até agora.")

            if count >= max_reviews:
                break

            if count == prev_count:
                attempts += 1
            else:
                attempts = 0

            if attempts >= 5:
                print("[✓] Nenhuma nova avaliação carregando. Encerrando scroll.")
                break

            # Scrolla dentro do modal
            modal_container.evaluate("(el) => el.scrollBy(0, el.scrollHeight)")
            page.wait_for_timeout(1500)
            prev_count = count

        print("[→] Extraindo avaliações...")
        for i in range(min(count, max_reviews)):
            article = articles.nth(i)
            text = article.locator('p.ui-review-capability-comments__comment__content').inner_text().strip()
            if text:
                data.append({
                    "review_text": text,
                    "source": "Mercado Livre"
                })

        browser.close()

    # Salva em JSON
    with open("ml_reviews.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[✓] {len(data)} avaliações salvas no arquivo ml_reviews.json")

if __name__ == "__main__":
    scrape_reviews("https://www.mercadolivre.com.br/aparador-de-grama-tramontina-ap1500t-com-dimetro-de-corte-280mm-1500w-laranjapreto/p/MLB9086770")
