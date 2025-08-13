import { Router } from "express";
import { PrismaClient } from "@prisma/client";
import axios from "axios";

const r = Router();
const prisma = new PrismaClient();
const AI_BASE = process.env.AI_BASE_URL || "http://ai:8000";

r.post('/analysis', async (req, res) => {
  const { imageId } = req.body as { imageId: string };
  const analysis = await prisma.analysis.create({ data: { imageId, resultJson: {}, status: 'processing' } });

  // fire-and-forget cập nhật kết quả
  axios.post(`${AI_BASE}/analysis`, { image_url: imageId, options: { detect_landmarks: true } })
    .then(async ({ data }) => {
      await prisma.analysis.update({ where: { id: analysis.id }, data: {
        resultJson: data,
        overlayUrl: data.overlay_url ?? null,
        durationMs: data.duration_ms ?? 0,
        status: 'done'
      }});
    })
    .catch(async () => {
      await prisma.analysis.update({ where: { id: analysis.id }, data: { status: 'failed' }});
    });

  return res.status(202).json({ analysis_id: analysis.id, status: analysis.status });
});

r.get('/analysis/:id', async (req, res) => {
  const an = await prisma.analysis.findUnique({ where: { id: req.params.id } });
  if (!an) return res.status(404).json({ message: 'Not found' });
  return res.json(an);
});

export default r;