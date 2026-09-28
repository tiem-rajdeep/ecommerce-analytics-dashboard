import streamlit as st
import plotly.express as px

from queries import (
    get_customer_segments,
    get_customer_lifetime_value
)


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("👥 Customer Analytics")

st.markdown(
    "Understand customer purchasing behavior and lifetime value."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

customer_segments = get_customer_segments()

customer_lifetime_value = get_customer_lifetime_value()


# ==================================================
# CUSTOMER SEGMENTATION
# ==================================================

st.markdown("---")

st.subheader("👥 Customer Segmentation")


col1, col2 = st.columns(2)


with col1:

    st.dataframe(
        customer_segments,
        use_container_width=True,
        hide_index=True
    )


with col2:

    fig_segments = px.pie(
        customer_segments,
        names="customer_type",
        values="customer_count",
        title="One-Time vs Repeat Buyers"
    )

    st.plotly_chart(
        fig_segments,
        use_container_width=True
    )


# ==================================================
# TOP CUSTOMERS
# ==================================================

st.markdown("---")

st.subheader("🏆 Top Customers by Lifetime Value")


st.dataframe(
    customer_lifetime_value,
    use_container_width=True,
    hide_index=True
)


# ==================================================
# LIFETIME VALUE CHART
# ==================================================

fig_ltv = px.bar(
    customer_lifetime_value.head(10),
    x="lifetime_value",
    y="customer_name",
    orientation="h",
    title="Top 10 Customers by Lifetime Value"
)

fig_ltv.update_layout(
    xaxis_title="Lifetime Value (₹)",
    yaxis_title="Customer"
)

st.plotly_chart(
    fig_ltv,
    use_container_width=True
)