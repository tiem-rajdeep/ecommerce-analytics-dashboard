import streamlit as st

from queries import (
    get_total_revenue,
    get_total_orders,
    get_average_order_value,
    get_active_customers,
    get_monthly_sales
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Overview | E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("📊 Business Overview")

st.markdown(
    "Monitor the overall performance of your e-commerce business."
)


# --------------------------------------------------
# GET DATA
# --------------------------------------------------

total_revenue = get_total_revenue()
total_orders = get_total_orders()
average_order_value = get_average_order_value()
active_customers = get_active_customers()

monthly_sales = get_monthly_sales()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.2f}"
    )


with col2:
    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )


with col3:
    st.metric(
        "📦 Average Order Value",
        f"₹{average_order_value:,.2f}"
    )


with col4:
    st.metric(
        "👥 Active Customers",
        f"{active_customers:,}"
    )


# --------------------------------------------------
# SALES TREND
# --------------------------------------------------

st.markdown("---")

st.subheader("📈 Monthly Revenue")

st.line_chart(
    monthly_sales,
    x="month",
    y="revenue"
)