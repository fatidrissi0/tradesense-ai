BEGIN;

CREATE TABLE user (
  id INTEGER PRIMARY KEY,
  username VARCHAR(80) UNIQUE NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) DEFAULT 'user',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE challenge (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  plan_type VARCHAR(20) NOT NULL,
  initial_balance FLOAT NOT NULL,
  current_balance FLOAT NOT NULL,
  daily_start_balance FLOAT NOT NULL,
  status VARCHAR(20) DEFAULT 'active',
  profit_target FLOAT DEFAULT 10.0,
  max_daily_loss_percent FLOAT DEFAULT 5.0,
  max_total_loss_percent FLOAT DEFAULT 10.0,
  started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  ended_at DATETIME,
  FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE trade (
  id INTEGER PRIMARY KEY,
  challenge_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  symbol VARCHAR(20) NOT NULL,
  action VARCHAR(10) NOT NULL,
  quantity FLOAT NOT NULL,
  price FLOAT NOT NULL,
  profit_loss FLOAT DEFAULT 0.0,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (challenge_id) REFERENCES challenge(id) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE,
  CHECK (action IN ('buy','sell'))
);

CREATE TABLE payment (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL,
  amount FLOAT NOT NULL,
  currency VARCHAR(10) DEFAULT 'DH',
  payment_method VARCHAR(20) NOT NULL,
  status VARCHAR(20) DEFAULT 'pending',
  transaction_id VARCHAR(100) UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(id) ON UPDATE CASCADE ON DELETE CASCADE,
  CHECK (status IN ('pending','completed','failed','refunded'))
);

COMMIT;
BEGIN;

INSERT INTO "user" (id, username, email, password_hash, role, is_active, created_at) VALUES
  (6, 'laila_pro', 'laila@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-06 09:10:00'),
  (7, 'omar_elite', 'omar@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-07 09:15:00'),
  (8, 'nadia_trader', 'nadia@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-08 09:20:00'),
  (9, 'hicham_fx', 'hicham@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-05 09:25:00'),
  (10, 'salma_crypto', 'salma@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-12 09:30:00');

INSERT INTO challenge (id, user_id, plan_type, initial_balance, current_balance, daily_start_balance, status, profit_target, max_daily_loss_percent, max_total_loss_percent, started_at, ended_at) VALUES
  (9,  6, 'pro',     10000, 10800, 10400, 'active', 10.0, 5.0, 10.0, '2026-01-07 10:00:00', NULL),
  (10, 7, 'elite',   25000, 26250, 25500, 'active', 10.0, 5.0, 10.0, '2026-01-07 11:00:00', NULL),
  (11, 8, 'starter',  5000,  5350,  5200, 'active', 10.0, 5.0, 10.0, '2026-01-08 09:00:00', NULL),
  (12, 9, 'pro',     10000,  9700,  9800, 'active', 10.0, 5.0, 10.0, '2026-01-08 10:00:00', NULL),
  (13,10, 'elite',   25000, 24000, 24500, 'active', 10.0, 5.0, 10.0, '2026-01-09 12:00:00', NULL);

INSERT INTO trade (id, challenge_id, user_id, symbol, action, quantity, price, profit_loss, timestamp) VALUES
  (29,  9, 6, 'AAPL',     'buy', 15, 175.00,   0.00, '2026-01-10 09:00:00'),
  (30,  9, 6, 'AAPL',     'sell',15, 178.00,  45.00, '2026-01-10 12:00:00'),
  (31,  9, 6, 'BTC-USD',  'sell',0.05,46200.00,600.00,'2026-01-11 15:00:00'),

  (32, 10, 7, 'TSLA',     'sell', 8, 252.00,  56.00, '2026-01-11 11:00:00'),
  (33, 10, 7, 'BTC-USD',  'sell',0.05,46000.00,500.00,'2026-01-12 10:00:00'),
  (34, 10, 7, 'AAPL',     'sell',30, 176.00,  30.00, '2026-01-13 13:00:00'),

  (35, 11, 8, 'AAPL',     'sell',20, 177.00,  40.00, '2026-01-09 10:00:00'),
  (36, 11, 8, 'ETH-USD',  'sell', 1, 2550.00,  50.00, '2026-01-10 09:30:00'),

  (37, 12, 9, 'TSLA',     'sell', 5, 242.00, -40.00, '2026-01-12 14:00:00'),
  (38, 12, 9, 'BTC-USD',  'sell',0.03,44000.00,-150.00,'2026-01-13 16:00:00'),

  (39, 13,10, 'ETH-USD',  'sell', 3, 2400.00,-300.00,'2026-01-11 11:30:00'),
  (40, 13,10, 'AAPL',     'sell',20, 170.00, -60.00, '2026-01-12 12:30:00');

COMMIT;

BEGIN;

INSERT INTO "user" (id, username, email, password_hash, role, is_active, created_at) VALUES
  (1, 'fatima_trader', 'fatima@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-08 09:10:00'),
  (2, 'ahmed_pro', 'ahmed@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-08 09:15:00'),
  (3, 'sarah_elite', 'sarah@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-08 09:20:00'),
  (4, 'karim_starter', 'karim@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-08 09:25:00'),
  (5, 'youssef_winner', 'youssef@test.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7QDUHF7S6W', 'user', TRUE, '2026-01-08 09:30:00');

INSERT INTO challenge (id, user_id, plan_type, initial_balance, current_balance, daily_start_balance, status, profit_target, max_daily_loss_percent, max_total_loss_percent, started_at, ended_at) VALUES
  (1, 1, 'pro',     10000, 11200, 11000, 'passed', 10.0, 5.0, 10.0, '2026-01-09 10:00:00', '2026-01-13 16:00:00'),
  (2, 5, 'elite',   25000, 27500, 27000, 'passed', 10.0, 5.0, 10.0, '2026-01-09 10:00:00', '2026-01-12 15:00:00'),
  (3, 2, 'starter',  5000,  5600,  5400, 'passed', 10.0, 5.0, 10.0, '2026-01-09 11:00:00', '2026-01-10 17:00:00'),
  (4, 3, 'pro',     10000, 10450, 10300, 'active', 10.0, 5.0, 10.0, '2026-01-11 09:00:00', NULL),
  (5, 4, 'starter',  5000,  5200,  5150, 'active', 10.0, 5.0, 10.0, '2026-01-11 09:30:00', NULL),
  (6, 2, 'pro',     10000,  9800,  9900, 'active', 10.0, 5.0, 10.0, '2026-01-11 10:00:00', NULL),
  (7, 4, 'starter',  5000,  4500,  4700, 'failed', 10.0, 5.0, 10.0, '2026-01-08 12:00:00', '2026-01-09 16:00:00'),
  (8, 1, 'pro',     10000,  9450, 10000, 'failed', 10.0, 5.0, 10.0, '2026-01-08 13:00:00', '2026-01-09 16:30:00');

INSERT INTO trade (id, challenge_id, user_id, symbol, action, quantity, price, profit_loss, timestamp) VALUES
  -- Challenge 1 (fatima_trader, passed): 10 trades, total profit ≈ +1200
  (1,  1, 1, 'AAPL',     'buy', 10, 175.50,   0.00, '2026-01-10 10:00:00'),
  (2,  1, 1, 'AAPL',     'sell',10, 178.25,  27.50, '2026-01-10 14:00:00'),
  (3,  1, 1, 'TSLA',     'buy',  5, 245.00,   0.00, '2026-01-11 09:20:00'),
  (4,  1, 1, 'TSLA',     'sell', 5, 252.00,  35.00, '2026-01-11 13:30:00'),
  (5,  1, 1, 'BTC-USD',  'buy',0.05,45000.00, 0.00, '2026-01-12 10:05:00'),
  (6,  1, 1, 'BTC-USD',  'sell',0.05,46500.00,750.00,'2026-01-12 16:10:00'),
  (7,  1, 1, 'ETH-USD',  'buy',  2, 2450.00,  0.00, '2026-01-12 11:00:00'),
  (8,  1, 1, 'ETH-USD',  'sell', 2, 2520.00,140.00, '2026-01-12 15:00:00'),
  (9,  1, 1, 'GOOGL',    'buy', 20, 140.00,   0.00, '2026-01-13 09:40:00'),
  (10, 1, 1, 'GOOGL',    'sell',20, 141.50, 30.00,  '2026-01-13 12:40:00'),

  -- Challenge 8 (fatima_trader, failed daily): 5 trades, total loss ≈ -376
  (11, 8, 1, 'TSLA',     'sell', 4, 240.00, -32.00, '2026-01-09 10:00:00'),
  (12, 8, 1, 'BTC-USD',  'sell',0.02,44500.00,-200.00,'2026-01-09 12:00:00'),
  (13, 8, 1, 'ETH-USD',  'sell', 2, 2500.00,-100.00,'2026-01-09 13:00:00'),
  (14, 8, 1, 'AAPL',     'sell',10, 171.00, -50.00, '2026-01-09 14:00:00'),
  (15, 8, 1, 'TSLA',     'sell', 3, 202.00,-144.00, '2026-01-09 15:30:00'),

  -- Challenge 2 (youssef_winner, passed): 7 trades, total profit ≈ +2425
  (16, 2, 5, 'BTC-USD',  'sell',0.10,46500.00,1500.00,'2026-01-11 10:00:00'),
  (17, 2, 5, 'ETH-USD',  'sell', 5, 2600.00, 500.00, '2026-01-11 12:00:00'),
  (18, 2, 5, 'AAPL',     'sell',30, 176.50,  45.00, '2026-01-11 13:00:00'),
  (19, 2, 5, 'TSLA',     'sell',10, 250.00,  50.00, '2026-01-11 14:00:00'),
  (20, 2, 5, 'GOOGL',    'sell',50, 141.00,  50.00, '2026-01-11 15:00:00'),
  (21, 2, 5, 'BTC-USD',  'sell',0.02,46000.00, 160.00,'2026-01-12 10:30:00'),
  (22, 2, 5, 'ETH-USD',  'sell', 3, 2525.00, 135.00, '2026-01-12 12:30:00'),

  -- Challenge 3 (ahmed_pro, passed): 4 trades, total profit ≈ +395
  (23, 3, 2, 'BTC-USD',  'sell',0.02,46500.00,300.00,'2026-01-10 11:00:00'),
  (24, 3, 2, 'AAPL',     'sell',10, 178.00,  25.00, '2026-01-10 12:00:00'),
  (25, 3, 2, 'TSLA',     'sell', 4, 250.00,  20.00, '2026-01-10 13:00:00'),
  (26, 3, 2, 'ETH-USD',  'sell', 1, 2550.00,  50.00, '2026-01-10 14:00:00'),

  -- Challenge 5 (karim_starter, active): 1 trade (Maroc)
  (27, 5, 4, 'IAM',      'sell',20, 145.00, 200.00, '2026-01-12 10:30:00'),

  -- Challenge 6 (ahmed_pro, active): 1 trade loss
  (28, 6, 2, 'TSLA',     'sell', 4, 245.00, -20.00, '2026-01-13 10:00:00');

INSERT INTO payment (id, user_id, amount, currency, payment_method, status, transaction_id, created_at) VALUES
  (1, 1,  500.00, 'DH', 'CMI',    'completed', 'TXN-20260110-001', '2026-01-10 09:00:00'),
  (2, 2,  200.00, 'DH', 'Crypto', 'completed', 'TXN-20260110-002', '2026-01-10 09:05:00'),
  (3, 3, 1000.00, 'DH', 'PayPal', 'completed', 'TXN-20260110-003', '2026-01-10 09:10:00'),
  (4, 4,  200.00, 'DH', 'CMI',    'completed', 'TXN-20260110-004', '2026-01-10 09:15:00'),
  (5, 5, 1000.00, 'DH', 'Crypto', 'completed', 'TXN-20260110-005', '2026-01-10 09:20:00');

COMMIT;
