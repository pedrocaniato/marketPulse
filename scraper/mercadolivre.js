import axios from "axios";
import * as cheerio from "cheerio";
import prisma from "../prisma/client.js"; // ajuste o caminho pro seu client do Prisma

// Função para scrapear reviews de um produto específico do Mercado Livre
export async function scrapeMercadoLivre(productUrl) {
  try {
    const { data: html } = await axios.get(productUrl);
    const $ = cheerio.load(html);

    const reviews = [];

    $(".ui-review-capability-comments__comment").each((i, el) => {
      const reviewText = $(el).find(".ui-review-capability-comments__comment__content").text().trim();
      const rating = $(el).find(".ui-star-rating").attr("title") || null;

      if (reviewText) {
        reviews.push({
          reviewText,
          sentiment: rating ? parseInt(rating) >= 4 ? "positive" : "negative" : "neutral",
          source: "Mercado Livre"
        });
      }
    });

    console.log(`🔍 Encontradas ${reviews.length} reviews`);

    // Salva no banco via Prisma
    for (const r of reviews) {
      await prisma.review.create({ data: r });
    }

    console.log("✅ Reviews salvos no banco!");
  } catch (err) {
    console.error("❌ Erro no scraping:", err.message);
  }
}