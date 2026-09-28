import random
from datetime import datetime, timedelta

try:
    import mysql.connector
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing MySQL connector. Install the project dependencies with: "
        "python -m pip install -r requirements.txt"
    ) from exc

from faker import Faker


# ============================================================
# CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Tiem@2004",
    "database": "ecommerce_analytics"
}

NUM_CUSTOMERS = 3000
NUM_ORDERS = 15000
NUM_REVIEWS = 8000

fake = Faker("en_IN")


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """
    Generate a random datetime between two dates.
    """

    delta = end_date - start_date

    random_days = random.randint(0, delta.days)

    return start_date + timedelta(
        days=random_days,
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )


# ============================================================
# GENERATE CUSTOMERS
# ============================================================

def generate_customers(connection):

    print("\nGenerating customers...")

    cursor = connection.cursor()

    query = """
        INSERT INTO customers
        (
            first_name,
            last_name,
            email,
            phone,
            city,
            state,
            country,
            registration_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    customers = []

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2026, 9, 1)

    for _ in range(NUM_CUSTOMERS):

        first_name = fake.first_name()
        last_name = fake.last_name()

        email = (
            first_name.lower()
            + "."
            + last_name.lower()
            + str(random.randint(1000, 99999))
            + "@example.com"
        )

        phone = fake.phone_number()

        city = fake.city()
        state = fake.state()

        registration_date = random_date(
            start_date,
            end_date
        ).date()

        customers.append((
            first_name,
            last_name,
            email,
            phone,
            city,
            state,
            "India",
            registration_date
        ))

    cursor.executemany(query, customers)

    connection.commit()

    print(f"{len(customers)} customers inserted.")

    cursor.close()


# ============================================================
# GET PRODUCTS
# ============================================================

def get_products(connection):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            price,
            stock_quantity
        FROM products
    """)

    products = cursor.fetchall()

    cursor.close()

    return products


# ============================================================
# GET CUSTOMERS
# ============================================================

def get_customers(connection):

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            customer_id,
            registration_date
        FROM customers
    """)

    customers = cursor.fetchall()

    cursor.close()

    return customers


# ============================================================
# GENERATE ORDERS + ORDER ITEMS + PAYMENTS
# ============================================================

def generate_orders(connection, customers, products):

    print("\nGenerating orders...")

    order_cursor = connection.cursor()

    order_query = """
        INSERT INTO orders
        (
            customer_id,
            order_date,
            order_status,
            total_amount
        )
        VALUES (%s, %s, %s, %s)
    """

    item_query = """
        INSERT INTO order_items
        (
            order_id,
            product_id,
            quantity,
            unit_price
        )
        VALUES (%s, %s, %s, %s)
    """

    payment_query = """
        INSERT INTO payments
        (
            order_id,
            payment_date,
            payment_method,
            payment_status,
            amount,
            transaction_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 9, 25)

    order_count = 0
    item_count = 0
    payment_count = 0

    for i in range(NUM_ORDERS):

        # ----------------------------------------------------
        # Select a customer
        # ----------------------------------------------------

        customer = random.choice(customers)

        customer_id = customer["customer_id"]

        registration_date = customer["registration_date"]

        # Don't create an order before customer registered
        minimum_order_date = max(
            datetime.combine(
                registration_date,
                datetime.min.time()
            ),
            start_date
        )

        order_date = random_date(
            minimum_order_date,
            end_date
        )

        # ----------------------------------------------------
        # Order status
        # ----------------------------------------------------

        order_status = random.choices(
            [
                "Pending",
                "Processing",
                "Shipped",
                "Delivered",
                "Cancelled"
            ],
            weights=[
                5,
                10,
                15,
                65,
                5
            ]
        )[0]

        # ----------------------------------------------------
        # Select products for this order
        # ----------------------------------------------------

        number_of_products = random.randint(1, 5)

        selected_products = random.sample(
            products,
            min(number_of_products, len(products))
        )

        order_items = []

        total_amount = 0

        for product in selected_products:

            product_id = product["product_id"]

            unit_price = float(product["price"])

            quantity = random.randint(1, 4)

            subtotal = unit_price * quantity

            total_amount += subtotal

            order_items.append((
                product_id,
                quantity,
                unit_price
            ))

        # ----------------------------------------------------
        # Insert order
        # ----------------------------------------------------

        order_cursor.execute(
            order_query,
            (
                customer_id,
                order_date,
                order_status,
                round(total_amount, 2)
            )
        )

        order_id = order_cursor.lastrowid

        order_count += 1

        # ----------------------------------------------------
        # Insert order items
        # ----------------------------------------------------

        for product_id, quantity, unit_price in order_items:

            order_cursor.execute(
                item_query,
                (
                    order_id,
                    product_id,
                    quantity,
                    unit_price
                )
            )

            item_count += 1

        # ----------------------------------------------------
        # Generate payment
        # ----------------------------------------------------

        payment_method = random.choice([
            "Credit Card",
            "Debit Card",
            "UPI",
            "Net Banking",
            "Cash on Delivery",
            "Wallet"
        ])

        if order_status == "Cancelled":

            payment_status = random.choice([
                "Failed",
                "Refunded"
            ])

        elif order_status == "Pending":

            payment_status = "Pending"

        else:

            payment_status = "Completed"

        transaction_id = (
            f"TXN"
            f"{random.randint(10000000, 99999999)}"
            f"{i}"
        )

        payment_amount = round(total_amount, 2)

        order_cursor.execute(
            payment_query,
            (
                order_id,
                order_date + timedelta(
                    minutes=random.randint(1, 60)
                ),
                payment_method,
                payment_status,
                payment_amount,
                transaction_id
            )
        )

        payment_count += 1

        # ----------------------------------------------------
        # Commit every 1000 orders
        # ----------------------------------------------------

        if (i + 1) % 1000 == 0:

            connection.commit()

            print(
                f"{i + 1:,} orders generated..."
            )

    connection.commit()

    print(f"{order_count:,} orders inserted.")
    print(f"{item_count:,} order items inserted.")
    print(f"{payment_count:,} payments inserted.")

    order_cursor.close()


# ============================================================
# GENERATE REVIEWS
# ============================================================

def generate_reviews(connection, customers, products):

    print("\nGenerating reviews...")

    cursor = connection.cursor()

    query = """
        INSERT INTO reviews
        (
            customer_id,
            product_id,
            rating,
            review_text,
            review_date
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    reviews = []

    used_combinations = set()

    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 9, 25)

    generated_count = 0

    review_texts = {
        1: [
            "Very disappointing product.",
            "Not worth the money.",
            "Quality was poor."
        ],
        2: [
            "Below my expectations.",
            "Could be better.",
            "Average quality."
        ],
        3: [
            "Decent product.",
            "Good but has some issues.",
            "Average overall."
        ],
        4: [
            "Very good product.",
            "Happy with the purchase.",
            "Good quality and value."
        ],
        5: [
            "Excellent product!",
            "Amazing quality!",
            "Highly recommended!",
            "Very satisfied with this purchase."
        ]
    }

    while generated_count < NUM_REVIEWS:

        customer = random.choice(customers)
        product = random.choice(products)

        customer_id = customer["customer_id"]
        product_id = product["product_id"]

        combination = (
            customer_id,
            product_id
        )

        # Prevent duplicate customer-product reviews
        if combination in used_combinations:
            continue

        used_combinations.add(combination)

        rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[3, 5, 12, 30, 50]
        )[0]

        review_text = random.choice(
            review_texts[rating]
        )

        review_date = random_date(
            start_date,
            end_date
        )

        reviews.append((
            customer_id,
            product_id,
            rating,
            review_text,
            review_date
        ))

        generated_count += 1

        # Insert every 1,000 reviews
        if len(reviews) >= 1000:

            cursor.executemany(
                query,
                reviews
            )

            connection.commit()

            print(
                f"{generated_count:,} reviews generated..."
            )

            reviews.clear()

    # Insert remaining reviews
    if reviews:

        cursor.executemany(
            query,
            reviews
        )

        connection.commit()

    print(
        f"{generated_count:,} reviews inserted."
    )

    cursor.close()


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("E-COMMERCE ANALYTICS DATA GENERATOR")
    print("=" * 60)

    connection = create_connection()

    try:

        print("\nConnected to MySQL successfully.")

        # ----------------------------------------------------
        # 1. Generate customers
        # ----------------------------------------------------

        generate_customers(connection)

        # ----------------------------------------------------
        # 2. Fetch customers and products
        # ----------------------------------------------------

        customers = get_customers(connection)
        products = get_products(connection)

        print(
            f"\nLoaded {len(customers):,} customers."
        )

        print(
            f"Loaded {len(products):,} products."
        )

        # ----------------------------------------------------
        # 3. Generate orders
        # ----------------------------------------------------

        generate_orders(
            connection,
            customers,
            products
        )

        # ----------------------------------------------------
        # 4. Generate reviews
        # ----------------------------------------------------

        generate_reviews(
            connection,
            customers,
            products
        )

        print("\n" + "=" * 60)
        print("DATA GENERATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:

        print("\nERROR:")
        print(e)

        connection.rollback()

    finally:

        connection.close()

        print("\nMySQL connection closed.")


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()