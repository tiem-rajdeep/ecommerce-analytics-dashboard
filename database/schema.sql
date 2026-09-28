-- ============================================================
-- E-COMMERCE ANALYTICS DATABASE
-- Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS ecommerce_analytics;

USE ecommerce_analytics;


-- ============================================================
-- 1. CATEGORIES
-- ============================================================

CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 2. PRODUCTS
-- ============================================================

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 10,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_category
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id),

    CONSTRAINT chk_product_price
        CHECK (price >= 0),

    CONSTRAINT chk_product_stock
        CHECK (stock_quantity >= 0)
);


-- ============================================================
-- 3. CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100) DEFAULT 'India',
    registration_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 4. ORDERS
-- ============================================================

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME NOT NULL,

    order_status ENUM(
        'Pending',
        'Processing',
        'Shipped',
        'Delivered',
        'Cancelled'
    ) DEFAULT 'Pending',

    total_amount DECIMAL(12,2) NOT NULL DEFAULT 0,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_order_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT chk_order_total
        CHECK (total_amount >= 0)
);


-- ============================================================
-- 5. ORDER ITEMS
-- ============================================================

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,

    subtotal DECIMAL(12,2)
        GENERATED ALWAYS AS (quantity * unit_price) STORED,

    CONSTRAINT fk_orderitem_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_orderitem_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT chk_orderitem_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_orderitem_price
        CHECK (unit_price >= 0)
);


-- ============================================================
-- 6. PAYMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_date DATETIME NOT NULL,

    payment_method ENUM(
        'Credit Card',
        'Debit Card',
        'UPI',
        'Net Banking',
        'Cash on Delivery',
        'Wallet'
    ) NOT NULL,

    payment_status ENUM(
        'Pending',
        'Completed',
        'Failed',
        'Refunded'
    ) DEFAULT 'Pending',

    amount DECIMAL(12,2) NOT NULL,

    transaction_id VARCHAR(100) UNIQUE,

    CONSTRAINT fk_payment_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT chk_payment_amount
        CHECK (amount >= 0)
);


-- ============================================================
-- 7. REVIEWS
-- ============================================================

CREATE TABLE IF NOT EXISTS reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL,
    review_text TEXT,
    review_date DATETIME NOT NULL,

    CONSTRAINT fk_review_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_review_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    CONSTRAINT chk_review_rating
        CHECK (rating BETWEEN 1 AND 5),

    CONSTRAINT uq_customer_product_review
        UNIQUE (customer_id, product_id)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_products_category
ON products(category_id);

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_orders_date
ON orders(order_date);

CREATE INDEX idx_orders_status
ON orders(order_status);

CREATE INDEX idx_order_items_order
ON order_items(order_id);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

CREATE INDEX idx_payments_order
ON payments(order_id);

CREATE INDEX idx_reviews_product
ON reviews(product_id);


-- ============================================================
-- VIEW: PRODUCT SALES SUMMARY
-- ============================================================

CREATE OR REPLACE VIEW product_sales_summary AS

SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    p.price,
    p.stock_quantity,

    COALESCE(
        SUM(oi.quantity),
        0
    ) AS units_sold,

    COALESCE(
        SUM(oi.subtotal),
        0
    ) AS revenue

FROM products p

JOIN categories c
    ON p.category_id = c.category_id

LEFT JOIN order_items oi
    ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name,
    c.category_name,
    p.price,
    p.stock_quantity;


-- ============================================================
-- STORED PROCEDURE: SALES BY DATE
-- ============================================================

DELIMITER //

CREATE PROCEDURE GetSalesByDate(
    IN start_date DATE,
    IN end_date DATE
)

BEGIN

    SELECT
        DATE(order_date) AS sale_date,

        COUNT(DISTINCT order_id)
            AS total_orders,

        SUM(total_amount)
            AS revenue,

        AVG(total_amount)
            AS average_order_value

    FROM orders

    WHERE DATE(order_date)
        BETWEEN start_date AND end_date

        AND order_status <> 'Cancelled'

    GROUP BY DATE(order_date)

    ORDER BY sale_date;

END //

DELIMITER ;