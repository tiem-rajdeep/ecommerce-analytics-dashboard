import pandas as pd
from database import get_connection


def get_total_revenue():
    query = """
        SELECT SUM(total_amount) AS total_revenue
        FROM orders
        WHERE order_status <> 'Cancelled';
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df.iloc[0]["total_revenue"]
    finally:
        connection.close()


def get_total_orders():
    query = """
        SELECT COUNT(*) AS total_orders
        FROM orders
        WHERE order_status <> 'Cancelled';
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df.iloc[0]["total_orders"]
    finally:
        connection.close()


def get_average_order_value():
    query = """
        SELECT AVG(total_amount) AS average_order_value
        FROM orders
        WHERE order_status <> 'Cancelled';
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df.iloc[0]["average_order_value"]
    finally:
        connection.close()


def get_active_customers():
    query = """
        SELECT COUNT(DISTINCT customer_id) AS active_customers
        FROM orders
        WHERE order_status <> 'Cancelled';
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df.iloc[0]["active_customers"]
    finally:
        connection.close()

def get_monthly_sales(start_date=None, end_date=None):

    query = """
        SELECT
            DATE_FORMAT(order_date, '%Y-%m') AS month,
            COUNT(DISTINCT order_id) AS total_orders,
            SUM(total_amount) AS revenue,
            AVG(total_amount) AS average_order_value
        FROM orders
        WHERE order_status <> 'Cancelled'
    """

    params = []

    if start_date:
        query += " AND DATE(order_date) >= %s"
        params.append(start_date)

    if end_date:
        query += " AND DATE(order_date) <= %s"
        params.append(end_date)

    query += """
        GROUP BY DATE_FORMAT(order_date, '%Y-%m')
        ORDER BY month;
    """

    connection = get_connection()

    try:
        df = pd.read_sql(
            query,
            connection,
            params=params
        )
        return df

    finally:
        connection.close()

def get_top_products():
    query = """
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
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()   

def get_customer_segments():
    query = """
        SELECT
            CASE
                WHEN order_count = 1 THEN 'One-Time Buyer'
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
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()

def get_customer_lifetime_value():
    query = """
        SELECT
            c.customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
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
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()

def get_low_stock_products():
    query = """
        SELECT
            p.product_id,
            p.product_name,
            c.category_name,
            p.stock_quantity,
            p.reorder_level,
            CASE
                WHEN p.stock_quantity = 0 THEN 'OUT OF STOCK'
                WHEN p.stock_quantity <= p.reorder_level THEN 'LOW STOCK'
                ELSE 'IN STOCK'
            END AS stock_status
        FROM products p
        JOIN categories c
            ON p.category_id = c.category_id
        WHERE p.stock_quantity <= p.reorder_level
        ORDER BY p.stock_quantity ASC;
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df
    finally:
        connection.close()

def get_categories():

    query = """
        SELECT category_name
        FROM categories
        ORDER BY category_name;
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df["category_name"].tolist()

    finally:
        connection.close()

def get_category_performance():

    query = """
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
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df

    finally:
        connection.close()

def get_payment_methods():

    query = """
        SELECT
            payment_method,
            COUNT(payment_id) AS total_transactions,
            SUM(amount) AS total_revenue

        FROM payments

        WHERE payment_status = 'Completed'

        GROUP BY payment_method

        ORDER BY total_revenue DESC;
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df

    finally:
        connection.close()

def get_order_status():

    query = """
        SELECT
            order_status,
            COUNT(*) AS order_count

        FROM orders

        GROUP BY order_status

        ORDER BY order_count DESC;
    """

    connection = get_connection()

    try:
        df = pd.read_sql(query, connection)
        return df

    finally:
        connection.close()