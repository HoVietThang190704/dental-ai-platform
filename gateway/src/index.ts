import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import uploads from './routes/uploads';
import analysis from './routes/analysis';
import authRoutes from './routes/authRoutes';

const app = express();
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(morgan('dev'));
app.get('/healthz', (_, res) => res.json({ status: 'ok' }));

app.use(uploads);
app.use('/v1', analysis);
app.use('/auth', authRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Gateway running on :${PORT}`));