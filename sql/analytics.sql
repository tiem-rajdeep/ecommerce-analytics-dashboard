USE ecommerce_analytics;


-- ============================================================
-- E-COMMERCE ANALYTICS SQL
-- ============================================================


-- ============================================================
-- 1. KPI - TOTAL REVENUE
-- ============================================================

SELECT
    SUM(total_amount) AS total_revenue
FROM orders
WHERE order_status <> 'Cancelled';


-- ============================================================
-- 2. KPI - TOTAL ORDERS
-- ============================================================

SELECT
    COUNT(*) AS total_orders
FROM orders
WHERE order_status <> 'Cancelled';


-- ============================================================
-- 3. KPI - AVERAGE ORDER VALUE
-- ============================================================

SELECT
    AVG(total_amount) AS average_order_value
FROM orders
WHERE order_status <> 'Cancelled';


-- ============================================================
-- 4. KPI - ACTIVE CUSTOMERS
-- ============================================================

SELECT
    COUNT(DISTINCT customer_id) AS active_customers
FROM orders
WHERE order_status <> 'Cancelled';


-- ============================================================
-- 5. MONTHLY REVENUE
-- ============================================================

SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(total_amount) AS revenue,
    AVG(total_amount) AS average_order_value
FROM orders
WHERE order_status <> 'Cancelled'
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;


-- ============================================================
-- 6. TOP 10 PRODUCTS
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.subtotal) AS revenue
FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

JOIN categories c
    ON p.category_id = c.category_id

JOIN orders o
    ON oi.order_id = o.order_id

WHERE o.order_status <> 'Cancelled'

GROUP BY
    p.product_id,
    p.product_name,
    c.category_name

ORDER BY revenue DESC

LIMIT 10;


-- ============================================================
-- 7. CATEGORY PERFORMANCE
-- ============================================================

SELECT
    c.category_id,
    c.category_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.subtotal) AS revenue
FROM order_items oi

JOIN products p
    ON oi.product_id = p.product_id

JOIN categories c
    ON p.category_id = c.category_id

JOIN orders o
    ON oi.order_id = o.order_id

WHERE o.order_status <> 'Cancelled'

GROUP BY
    c.category_id,
    c.category_name

ORDER BY revenue DESC;


-- ============================================================
-- 8. CUSTOMER LIFETIME VALUE
-- ============================================================

SELECT
    c.customer_id,

    CONCAT(
        c.first_name,
        ' ',
        c.last_name
    ) AS customer_name,

    COUNT(o.order_id) AS total_orders,

    SUM(o.total_amount) AS lifetime_value

FROM customers c

JOIN orders o
    ON c.customer_id = o.customer_id

WHERE o.order_status <> 'Cancelled'

GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name

ORDER BY lifetime_value DESC

LIMIT 20;


-- ============================================================
-- 9. REPEAT VS ONE-TIME CUSTOMERS
-- ============================================================

SELECT
    CASE
        WHEN order_count = 1
            THEN 'One-Time Buyer'
        ELSE 'Repeat Buyer'
    END AS customer_type,

    COUNT(*) AS customer_count

FROM (
    SELECT
        customer_id,
        COUNT(*) AS order_count

    FROM orders

    WHERE order_status <> 'Cancelled'

    GROUP BY customer_id

) customer_orders

GROUP BY customer_type;


-- ============================================================
-- 10. LOW STOCK PRODUCTS
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    c.category_name,
    p.stock_quantity,
    p.reorder_level,

    CASE
        WHEN p.stock_quantity = 0
            THEN 'OUT OF STOCK'

        WHEN p.stock_quantity <= p.reorder_level
            THEN 'LOW STOCK'

        ELSE 'IN STOCK'

    END AS stock_status

FROM products p

JOIN categories c
    ON p.category_id = c.category_id

WHERE p.stock_quantity <= p.reorder_level

ORDER BY p.stock_quantity ASC;


-- ============================================================
-- 11. PRODUCT RATING ANALYSIS
-- ============================================================

SELECT
    p.product_id,
    p.product_name,

    ROUND(
        AVG(r.rating),
        2
    ) AS average_rating,

    COUNT(r.review_id) AS total_reviews

FROM products p

LEFT JOIN reviews r
    ON p.product_id = r.product_id

GROUP BY
    p.product_id,
    p.product_name

ORDER BY average_rating DESC;


-- ============================================================
-- 12. PAYMENT METHOD ANALYSIS
-- ============================================================

SELECT
    payment_method,
    COUNT(payment_id) AS total_transactions,
    SUM(amount) AS total_revenue

FROM payments

WHERE payment_status = 'Completed'

GROUP BY payment_method

ORDER BY total_revenue DESC;


-- ============================================================
-- 13. ORDER STATUS ANALYSIS
-- ============================================================

SELECT
    order_status,
    COUNT(*) AS order_count

FROM orders

GROUP BY order_status

ORDER BY order_count DESC;


-- ============================================================
-- 14. NEW CUSTOMER ACQUISITION
-- ============================================================

SELECT
    DATE_FORMAT(
        registration_date,
        '%Y-%m'
    ) AS month,

    COUNT(*) AS new_customers

FROM customers

GROUP BY DATE_FORMAT(
    registration_date,
    '%Y-%m'
)

ORDER BY month;