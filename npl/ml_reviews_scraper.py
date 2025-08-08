from playwright.sync_api import sync_playwright, TimeoutError, ViewportSize
import json


def scrape_reviews(product_url, max_reviews=25):
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport=ViewportSize(width=1920, height=1080)
        )
        page = context.new_page()

        page.goto(product_url, timeout=60000)

        print("[→] Procurando botão 'Mostrar todas as opiniões'...")

        try:
            show_more_selector = 'button[data-testid="see-more"]'
            page.wait_for_selector(show_more_selector, state="visible", timeout=10000)
            page.wait_for_timeout(1000)  # espera 1 segundo extra para estabilizar, SE TIRAR ISSO AQUI F TOTAL NO CHAT
            page.locator(show_more_selector).click(force=True)
            print("[✓] Botão de avaliações clicado.")
        except Exception as e:
            print(f"[✘] Erro ao clicar no botão de avaliações: {e}")
            browser.close()
            return

        try:
            print("[→] Aguardando iframe de avaliações carregar...")
            iframe_selector = 'iframe[data-testid="ui-pdp-iframe-reviews"]'
            page.wait_for_selector(iframe_selector, timeout=15000)
            reviews_frame = page.frame_locator(iframe_selector)
            print("[✓] Iframe carregado.")

            reviews_frame.locator('article[data-testid="comment-component"]').first.wait_for(timeout=10000)
            print("[✓] Seção de avaliações carregada dentro do iframe.")

        except TimeoutError:
            print("[✘] O iframe ou a seção de avaliações não carregou após o clique.")
            browser.close()
            return

        print("[→] Scrollando dentro do iframe para carregar avaliações...")
        prev_count = 0
        attempts = 0

        while True:
            articles = reviews_frame.locator('article[data-testid="comment-component"]')
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

            articles.nth(-1).scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            prev_count = count

        print("[→] Extraindo avaliações...")
        final_articles = reviews_frame.locator('article[data-testid="comment-component"]')
        for i in range(min(final_articles.count(), max_reviews)):
            article = final_articles.nth(i)
            text_element = article.locator('p.ui-review-capability-comments__comment__content')
            if text_element.count() > 0:
                text = text_element.inner_text().strip()
                if text:
                    data.append({
                        "review_text": text,
                        "source": "Mercado Livre"
                    })

        browser.close()


    with open("ml_reviews.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[✓] {len(data)} avaliações salvas no arquivo ml_reviews.json")


if __name__ == "__main__":
    scrape_reviews(
        "https://www.mercadolivre.com.br/aparador-de-grama-tramontina-ap1500t-com-dimetro-de-corte-280mm-1500w-laranjapreto/p/MLB9086770")
