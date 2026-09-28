import streamlit as st


st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="🛍️",
    layout="wide"
)


st.title("🛍️ E-Commerce Analytics Dashboard")

st.markdown(
    """
    ## Welcome 👋

    Explore your e-commerce business performance using the
    navigation menu on the left.
    """
)


st.markdown("---")


st.subheader("📊 Dashboard Modules")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown("### 📊 Overview")

    st.write(
        "Monitor revenue, orders, AOV and active customers."
    )

    st.page_link(
        "pages/1_Overview.py",
        label="Explore Overview →",
        icon="📊"
    )


with col2:

    st.markdown("### 📈 Sales")

    st.write(
        "Analyze sales trends, products and categories."
    )

    st.page_link(
        "pages/2_Sales_Analytics.py",
        label="Explore Sales →",
        icon="📈"
    )


with col3:

    st.markdown("### 👥 Customers")

    st.write(
        "Analyze customer behavior and lifetime value."
    )

    st.page_link(
        "pages/3_Customer_Analytics.py",
        label="Explore Customers →",
        icon="👥"
    )


with col4:

    st.markdown("### 📦 Inventory")

    st.write(
        "Monitor low-stock products and inventory."
    )

    st.page_link(
        "pages/4_Inventory.py",
        label="Explore Inventory →",
        icon="📦"
    )