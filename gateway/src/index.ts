import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import uploads from './routes/uploads';
import analysis from './routes/analysis';

const app = express();
app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(morgan('dev'));
app.get('/healthz', (_, res) => res.json({ status: 'ok' }));

app.use(uploads);
app.use('/v1', analysis);

app.listen(3000, () => console.log('Gateway on :3000'));