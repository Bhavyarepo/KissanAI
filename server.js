const express = require('express');
const cors = require('cors');
const { createProxyMiddleware } = require('http-proxy-middleware');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
require('dotenv').config({ path: './backend/.env' }); // Load env variables from backend

const app = express();
const PORT = process.env.NODE_PORT || 5000;

// PostgreSQL Connection
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

app.use(cors());
// Note: We don't use express.json() globally because the proxy middleware needs the raw request body.
// We will only use it on our specific routes.

// --- Node.js Managed Routes (Authentication) ---
const authRouter = express.Router();
authRouter.use(express.json());

authRouter.post('/register', async (req, res) => {
  try {
    const { name, email, phone, location, state, district, village, password } = req.body;
    
    // Check if user exists
    const userCheck = await pool.query(
      'SELECT * FROM farmers WHERE email = $1 OR phone = $2',
      [email, phone]
    );
    
    if (userCheck.rows.length > 0) {
      return res.status(400).json({ detail: "Farmer with this email or phone already exists" });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert user
    const newUser = await pool.query(
      `INSERT INTO farmers (name, email, phone, location, state, district, village, hashed_password, is_active, created_at, updated_at) 
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, true, NOW(), NOW()) RETURNING id, name, email, phone`,
      [name, email, phone, location, state, district, village, hashedPassword]
    );

    res.json(newUser.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ detail: "Server error during registration" });
  }
});

authRouter.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    
    const user = await pool.query('SELECT * FROM farmers WHERE email = $1', [email]);
    
    if (user.rows.length === 0) {
      return res.status(401).json({ detail: "Incorrect email or password" });
    }

    const validPassword = await bcrypt.compare(password, user.rows[0].hashed_password);
    
    if (!validPassword) {
      return res.status(401).json({ detail: "Incorrect email or password" });
    }

    // Create JWT
    const token = jwt.sign(
      { sub: user.rows[0].id.toString() }, 
      process.env.SECRET_KEY || "your-secret-key-here-change-in-production",
      { expiresIn: '30m' }
    );

    res.json({ access_token: token, token_type: "bearer" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ detail: "Server error during login" });
  }
});

authRouter.get('/me', async (req, res) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader) return res.status(401).json({ detail: "Not authenticated" });
    
    const token = authHeader.split(' ')[1];
    const decoded = jwt.verify(token, process.env.SECRET_KEY || "your-secret-key-here-change-in-production");
    
    const user = await pool.query('SELECT id, name, email, phone, location, state, district, village FROM farmers WHERE id = $1', [decoded.sub]);
    
    if (user.rows.length === 0) return res.status(404).json({ detail: "User not found" });
    
    res.json(user.rows[0]);
  } catch (err) {
    res.status(401).json({ detail: "Invalid token" });
  }
});

app.use('/api/auth', authRouter);

// --- Proxy all other requests to Python Backend ---
const pythonBackendProxy = createProxyMiddleware({
  target: 'http://localhost:8000',
  changeOrigin: true,
  logLevel: 'debug'
});

// Any request starting with /api/ but NOT /api/auth goes to Python
app.all(/^\/api\/(recommendations|soil|market|notifications|detection).*$/, pythonBackendProxy);

// Start server
app.listen(PORT, () => {
  console.log(`Node.js API Gateway running on http://localhost:${PORT}`);
  console.log(`Proxying ML requests to Python Backend on http://localhost:8000`);
});
