import express from 'express';
import bodyParser from 'body-parser';
import jwt from 'jsonwebtoken';
import { Pool } from 'pg';

const app = express();
const port = 3001;
const SECRET = "your_jwt_secret"; // In real projects, keep this in env vars

app.use(bodyParser.json());

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'iam',
  password: 'yourpassword',
  port: 5432,
});

app.post('/login', async (req, res) => {
  const { email, password } = req.body;

  // Mock password check
  if (!email || !password) return res.status(400).json({ error: "Missing credentials" });

  try {
    const result = await pool.query('SELECT email, role FROM users WHERE email = $1', [email]);
    if (result.rows.length === 0) return res.status(401).json({ error: "Invalid credentials" });

    // You can enhance by checking password hash here
    const user = result.rows[0];
    const token = jwt.sign({ email: user.email, role: user.role }, SECRET, { expiresIn: '1h' });

    res.json({ token, role: user.role });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Internal server error" });
  }
});

const authMiddleware = (req, res, next) => {
  const authHeader = req.headers.authorization;
  if (!authHeader) return res.status(401).json({ error: "Missing token" });

  const token = authHeader.split(" ")[1];
  try {
    const decoded = jwt.verify(token, SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    return res.status(401).json({ error: "Invalid token" });
  }
};

app.get('/dashboard', authMiddleware, (req, res) => {
  const { role } = req.user;

  if (role === 'admin') {
    res.json({ message: "Welcome admin. Here is the admin dashboard." });
  } else if (role === 'user') {
    res.json({ message: "Welcome user. Here is your dashboard." });
  } else {
    res.status(403).json({ error: "Unauthorized role" });
  }
});

app.listen(port, () => {
  console.log(`IAM server listening on port ${port}`);
});