-- =======================================================
-- Test Data Management Initialization Script
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

-- Pre-seed predictable baseline test data
INSERT INTO products (name, description, price, stock) VALUES
('Test Gaming Laptop', 'High performance test laptop for integration testing', 1299.99, 10),
('Test Wireless Mouse', 'Ergonomic optical test mouse', 49.99, 50),
('Test Low Stock Gadget', 'Low inventory item for negative boundary testing', 89.00, 2);

-- Pre-seed an existing order for update/cancellation testing
INSERT INTO orders (product_id, quantity, total_amount, shipping_address, status, created_at) VALUES
(2, 2, 99.98, '100 Baseline Test Ave, Testing City', 'CONFIRMED', NOW());
