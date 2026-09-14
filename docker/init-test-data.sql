-- =======================================================
-- Test Data Management Initialization Script
-- Bakery & Pastry E-Commerce Domain (Currency: PHP - Philippine Peso)
-- Automatically loaded by Docker PostgreSQL container on startup
-- =======================================================

-- Create products table if not already created
CREATE TABLE IF NOT EXISTS products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    stock INTEGER NOT NULL
);

-- Create orders table if not already created
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    quantity INTEGER NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    shipping_address TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL
);

-- Clean existing test data before inserting fresh baseline
TRUNCATE TABLE orders, products RESTART IDENTITY CASCADE;

-- Pre-seed predictable baseline test data: Bakery Cookies & Pastries (PHP Currency)
INSERT INTO products (name, description, price, stock) VALUES
('Chocolate Chip Cookie Box', 'Freshly baked artisan cookies with Belgian chocolate chips - Box of 6 (PHP 250.00)', 250.00, 20),
('Ube Cheese Pandesal', 'Soft bakery pastry filled with creamy ube halaya and savory cheese - Box of 10 (PHP 180.00)', 180.00, 50),
('Matcha Cream Croissant', 'Flaky French butter croissant infused with Japanese Uji matcha cream - Limited Batch (PHP 140.00)', 140.00, 2);

-- Pre-seed an existing pastry order for update/cancellation testing (2 boxes of Ube Cheese Pandesal @ PHP 180 = PHP 360.00)
INSERT INTO orders (product_id, quantity, total_amount, shipping_address, status, created_at) VALUES
(2, 2, 360.00, 'Unit 12B, Katipunan Avenue, Quezon City, Metro Manila', 'CONFIRMED', NOW());
