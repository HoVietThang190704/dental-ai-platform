import e, { Router } from "express";
import crypto from "crypto";

const r = Router();

r.get('/uploads/:id', (req, res) => {
  const key = `u/${crypto.randomBytes(8).toString('hex')}/raw.jpg`;
  // TODO: ký pre-signed URL MinIO/S3; tạm thời trả mock
  return res.json({ url: `http://minio:9000/${process.env.S3_BUCKET}/${key}`, key });
});

export default r;