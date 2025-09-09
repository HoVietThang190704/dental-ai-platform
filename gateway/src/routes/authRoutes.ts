import { Router } from 'express';
import * as AuthService from '../services/authService';

const router = Router();

router.post('/register', async (req, res) => {
    try {
        const { email, password, name } = req.body || {};
        if (!email || !password) return res.status(400).json({ error: "Email & password required" });
        const user = await AuthService.register(email, password, name);
        return res.status(201).json({ user });
    } catch (err: any) {
    const msg = err.code === 'P2002' ? 'Email already registered' : err.message;
    res.status(400).json({ error: msg });
  }
});

router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body || {};
        if (!email || !password) return res.status(400).json({ error: 'email & password required' });
        const data = await AuthService.login(email, password);
        res.json(data);
    } catch (err: any) {
        res.status(400).json({ error: err.message });
    }
});

export default router;