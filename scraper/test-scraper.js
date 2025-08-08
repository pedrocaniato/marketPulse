import { scrapeMercadoLivre } from "./mercadolivre.js";

const url = "https://www.mercadolivre.com.br/cadeira-office-giratoria-presidente-columbus-rivatti-preto-material-do-estofamento-tela-mesh/p/MLB35735503#reviews";

scrapeMercadoLivre(url)
  .then(data => {
    console.log("Reviews coletados:", data);
  })
  .catch(err => {
    console.error("Erro ao coletar reviews:", err);
  });