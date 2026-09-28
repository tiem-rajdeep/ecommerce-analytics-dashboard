import streamlit as st
import plotly.express as px

from queries import (
    get_monthly_sales,
    get_top_products,
    get_category_performance,
    get_payment_methods,
    get_order_status
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📈 Sales Analytics")

st.markdown(
    "Analyze revenue, products, categories, payments and order performance."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

monthly_sales = get_monthly_sales()
top_products = get_top_products()
category_performance = get_category_performance()
payment_methods = get_payment_methods()
order_status = get_order_status()


# ==================================================
# MONTHLY REVENUE
# ==================================================

st.markdown("---")

st.subheader("📈 Monthly Revenue")

fig_revenue = px.line(
    monthly_sales,
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

fig_revenue.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (₹)",
    hovermode="x unified"
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)


# ==================================================
# TOP PRODUCTS
# ==================================================

st.markdown("---")

st.subheader("🏆 Top 10 Products")


col1, col2 = st.columns(2)


with col1:

    st.dataframe(
        top_products,
        use_container_width=True,
        hide_index=True
    )


with col2:

    fig_products = px.bar(
        top_products,
        x="revenue",
        y="product_name",
        orientation="h",
        title="Top Products by Revenue"
    )

    fig_products.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Product",
        yaxis={
            "categoryorder": "total ascending"
        }
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


# ==================================================
# CATEGORY PERFORMANCE
# ==================================================

st.markdown("---")

st.subheader("🛍️ Category Performance")


col1, col2 = st.columns(2)


with col1:

    fig_category = px.bar(
        category_performance,
        x="category_name",
        y="revenue",
        title="Revenue by Category"
    )

    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Revenue (₹)"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    fig_category_pie = px.pie(
        category_performance,
        names="category_name",
        values="revenue",
        title="Revenue Distribution"
    )

    st.plotly_chart(
        fig_category_pie,
        use_container_width=True
    )


# ==================================================
# PAYMENT METHODS
# ==================================================

st.markdown("---")

st.subheader("💳 Payment Method Analysis")


fig_payment = px.bar(
    payment_methods,
    x="payment_method",
    y="total_revenue",
    title="Revenue by Payment Method"
)

fig_payment.update_layout(
    xaxis_title="Payment Method",
    yaxis_title="Revenue (₹)"
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)


# ==================================================
# ORDER STATUS
# ==================================================

st.markdown("---")

st.subheader("📦 Order Status")


fig_status = px.pie(
    order_status,
    names="order_status",
    values="order_count",
    title="Order Status Distribution"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)