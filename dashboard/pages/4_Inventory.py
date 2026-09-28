import streamlit as st
import plotly.express as px

from queries import get_low_stock_products


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Inventory",
    page_icon="📦",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📦 Inventory Analytics")

st.markdown(
    "Monitor products that require restocking."
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

low_stock_products = get_low_stock_products()


# --------------------------------------------------
# KPI
# --------------------------------------------------

if low_stock_products.empty:

    st.success("✅ No low-stock products.")

else:

    st.warning(
        f"⚠️ {len(low_stock_products)} products require attention."
    )


# --------------------------------------------------
# INVENTORY TABLE
# --------------------------------------------------

st.markdown("---")

st.subheader("⚠️ Low Stock Products")


if not low_stock_products.empty:

    st.dataframe(
        low_stock_products,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("All products have sufficient stock.")


# --------------------------------------------------
# STOCK CHART
# --------------------------------------------------

if not low_stock_products.empty:

    st.markdown("---")

    st.subheader("📊 Stock Level")


    fig_stock = px.bar(
        low_stock_products,
        x="product_name",
        y="stock_quantity",
        color="stock_status",
        title="Products Requiring Attention"
    )

    fig_stock.update_layout(
        xaxis_title="Product",
        yaxis_title="Stock Quantity"
    )

    st.plotly_chart(
        fig_stock,
        use_container_width=True
    )