# 🛍️ E-Commerce Analytics Dashboard

> An interactive business intelligence dashboard built with MySQL and Python (Streamlit) to analyse e-commerce KPIs, sales trends, customer behaviour, and inventory health.

---

## 📌 Overview

This project is a full-stack data analytics application that connects a **normalized MySQL relational database** to an interactive **multi-page Streamlit dashboard**. It was built as a portfolio project to demonstrate practical skills in SQL schema design, analytical query writing, and Python-based data visualization.

The application simulates a real-world e-commerce business with synthetic data generated via the Faker library. It covers the complete analytics lifecycle — from raw database design and stored procedures, to a polished, browser-based dashboard.

---

## ✨ Features

### 📊 Business Overview
- **KPI cards** displaying Total Revenue, Total Orders, Average Order Value (AOV), and Active Customers
- **Monthly Revenue Trend** line chart showing business growth over time

### 📈 Sales Analytics
- **Monthly Revenue** interactive line chart with markers and hover tooltips
- **Top 10 Products** by revenue — horizontal bar chart + sortable data table
- **Category Performance** — bar chart and pie chart showing revenue distribution across product categories
- **Payment Method Analysis** — breakdown of revenue by payment method (Credit Card, UPI, Net Banking, etc.)
- **Order Status Distribution** — pie chart of Pending, Processing, Shipped, Delivered, and Cancelled orders

### 👥 Customer Analytics
- **Customer Segmentation** — One-Time vs. Repeat Buyer breakdown (pie chart + table)
- **Customer Lifetime Value (CLV)** — Top 20 customers ranked by total spend, with horizontal bar chart for top 10

### 📦 Inventory Management
- **Low Stock Alert** — dynamic warning banner showing count of products requiring attention
- **Low Stock Products Table** — filterable view with `stock_quantity`, `reorder_level`, and computed `stock_status`
- **Stock Level Chart** — color-coded bar chart distinguishing `OUT OF STOCK` vs. `LOW STOCK` products

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Database** | MySQL 8.0 |
| **Backend / Queries** | Python 3.10+, `mysql-connector-python` |
| **Data Manipulation** | `pandas` |
| **Dashboard Framework** | `streamlit` |
| **Visualizations** | `plotly.express` |
| **Data Generation** | `faker` |
| **Config Management** | `python-dotenv` |

---

## 🗄️ Database Schema

The database (`ecommerce_analytics`) consists of **7 normalized tables** with enforced foreign keys, CHECK constraints, and strategic indexes.

```
categories ──┐
             ├──► products ──┐
                             ├──► order_items ◄── orders ◄── customers
             └──► reviews ◄──┘                         └──► payments
```

| Table | Description |
|---|---|
| `categories` | Product categories (e.g., Electronics, Apparel) |
| `products` | Product catalog with price, stock quantity, and reorder level |
| `customers` | Customer profiles with location and registration date |
| `orders` | Order headers with status (`Pending`, `Processing`, `Shipped`, `Delivered`, `Cancelled`) and total amount |
| `order_items` | Line items per order; `subtotal` is a **generated column** (`quantity × unit_price`) |
| `payments` | Payment records per order with method and status |
| `reviews` | One review per customer-product pair, with 1–5 star rating |

**Additional database objects:**
- **View** — `product_sales_summary`: Pre-aggregated product revenue and units sold across all non-cancelled orders
- **Stored Procedure** — `GetSalesByDate(start_date, end_date)`: Returns daily order count, revenue, and AOV for a given date range
- **Indexes** — 8 performance indexes on high-cardinality join and filter columns (`order_date`, `order_status`, `customer_id`, `product_id`, etc.)

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.10+
- MySQL 8.0 server running locally
- `pip`

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ecommerce-analytics.git
cd ecommerce-analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install streamlit pandas plotly python-dotenv
```

### 4. Configure the Database Connection

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ecommerce_analytics
```

### 5. Initialize the Database Schema

Open a terminal and run:

```bash
mysql -u root -p < database/schema.sql
```

This creates the `ecommerce_analytics` database, all tables, indexes, the view, and the stored procedure.

### 6. Generate Synthetic Data

```bash
python scripts/generate_data.py
```

This populates the database with realistic fake records using the Faker library.

### 7. Launch the Dashboard

```bash
cd dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📸 Screenshots

### Home Page
<img width="100%" alt="homepage" src="https://github.com/user-attachments/assets/ea9f1629-df05-484d-8dff-261bf086f46a">

### Business Overview
<img width="100%" alt="Business-Overview" src="https://github.com/user-attachments/assets/5b233bc5-4a1a-4684-a2a9-6c044de595f3">

### Sales Analytics
<img width="100%" alt="Sales-Analytics" src="https://github.com/user-attachments/assets/0f8e5dea-ba08-49a1-86ee-61ea93467e74">

### Customer Analytics
<img width="100%" alt="Customer-Analytics" src="https://github.com/user-attachments/assets/1231faa4-a030-4219-8e48-c6084529dc3f">

### Inventory Management
<img width="100%" alt="Inventory-Analytics" src="https://github.com/user-attachments/assets/1411d2d4-f03a-411b-864d-3dd078efac1e">

---

## 📁 Project Structure

```
ecommerce-analytics/
│
├── dashboard/                      # Streamlit application
│   ├── app.py                      # Entry point — home page & navigation
│   ├── database.py                 # MySQL connection factory (uses .env)
│   ├── queries.py                  # All SQL query functions returning DataFrames
│   ├── components.py               # Shared UI components
│   └── pages/
│       ├── 1_Overview.py           # KPI cards + monthly revenue trend
│       ├── 2_Sales_Analytics.py    # Revenue, top products, categories, payments
│       ├── 3_Customer_Analytics.py # CLV and customer segmentation charts
│       └── 4_Inventory.py          # Low-stock alerts and stock level chart
│
├── database/
│   └── schema.sql                  # Full DDL: tables, indexes, view, stored procedure
│
├── sql/
│   └── analytics.sql               # Standalone analytical queries (14 queries)
│
├── scripts/
│   └── generate_data.py            # Faker-based synthetic data generator
│
├── .env                            # Local DB credentials (not committed)
├── .gitignore
└── requirements.txt
```

---

## 💡 Key SQL & Python Highlights

- **Generated Column** — `order_items.subtotal` is defined as `GENERATED ALWAYS AS (quantity * unit_price) STORED`, ensuring subtotals are always consistent without any application-layer computation, and the value is persisted for fast reads.

- **Subquery-based Customer Segmentation** — The repeat vs. one-time buyer query uses a derived table that groups orders per customer, then applies a `CASE` expression on the outer query to classify segments — avoiding a `HAVING` clause and keeping the logic clean and extendable.

- **Parameterized Date Filtering** — `get_monthly_sales()` in `queries.py` dynamically appends `WHERE` clauses using parameterized inputs (`%s`) rather than string formatting, which prevents SQL injection while keeping the date filter extensible for future dashboard controls.

---

## 👤 Author

**RAJDEEP SAHA** B.Tech Computer Science & Engineering
- GitHub: [@tiem-rajdeep](https://github.com/tiem-rajdeep)
- LinkedIn: [RAJDEEP SAHA](https://www.linkedin.com/in/rajdeep-saha-29929327b)

---

## 📄 License

This project is licensed under a custom restrictive license (All Rights Reserved) — see the [LICENSE](file:///c:/Users/souna/OneDrive/Documents/Desktop/ecommerce-analytics/LICENSE) file for full details. Personal viewing and educational demonstration are permitted; commercial reproduction or redistribution without explicit permission is strictly prohibited.

---

> *Built as a portfolio project to demonstrate skills in relational database design, analytical SQL, and Python data application development.*
