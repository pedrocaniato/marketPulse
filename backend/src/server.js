const express = require('express');
const { PrismaClient } = require('@prisma/client');
const cors = require('cors');

const prisma = new PrismaClient();
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

// Rota básica para testar
app.get('/', (req, res) => {
  res.send('API MarketPulse rodando!');
});

// ✅ GET /reviews com filtros e paginação
app.get('/reviews', async (req, res) => {
  const { sentiment, source, page = 1, limit = 10 } = req.query;

  const filters = {};
  if (sentiment) filters.sentiment = sentiment;
  if (source) filters.source = source;

  const skip = (Number(page) - 1) * Number(limit);

  try {
    const [reviews, total] = await Promise.all([
      prisma.review.findMany({
        where: filters,
        orderBy: { createdAt: 'desc' },
        skip,
        take: Number(limit),
      }),
      prisma.review.count({ where: filters }),
    ]);

    res.json({
      total,
      page: Number(page),
      limit: Number(limit),
      totalPages: Math.ceil(total / Number(limit)),
      reviews,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao buscar reviews' });
  }
});

// GET review por ID
app.get('/reviews/:id', async (req, res) => {
  const { id } = req.params;
  try {
    const review = await prisma.review.findUnique({
      where: { id: Number(id) },
    });
    if (!review) {
      return res.status(404).json({ error: 'Review não encontrado' });
    }
    res.json(review);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao buscar review' });
  }
});

// POST criar review
app.post('/reviews', async (req, res) => {
  const { reviewText, source, sentiment } = req.body;
  try {
    const newReview = await prisma.review.create({
      data: {
        reviewText,
        source,
        sentiment,
      },
    });
    res.status(201).json(newReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao criar review' });
  }
});

// ✅ DELETE /reviews/:id
app.delete('/reviews/:id', async (req, res) => {
  const { id } = req.params;
  try {
    await prisma.review.delete({
      where: { id: Number(id) },
    });
    res.json({ message: 'Review removido com sucesso!' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao deletar review' });
  }
});

// ✅ PATCH /reviews/:id
app.patch('/reviews/:id', async (req, res) => {
  const { id } = req.params;
  const { reviewText, sentiment, source } = req.body;

  try {
    const updated = await prisma.review.update({
      where: { id: Number(id) },
      data: {
        ...(reviewText && { reviewText }),
        ...(sentiment && { sentiment }),
        ...(source && { source }),
      },
    });
    res.json(updated);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Erro ao atualizar review' });
  }
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`✅ API rodando em http://localhost:${PORT}`);
});