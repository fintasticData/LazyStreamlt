import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the page layout to wide for better utilization of screen space
st.set_page_config(layout="wide")

# Setting the title of the dashboard
st.title("FMCG Sales Dashboard")

# Generate demo FMCG sales data
np.random.seed(42)

data = {
    "Product": np.random.choice(
        ["Soap", "Shampoo", "Toothpaste", "Detergent", "Juice", "Snacks"], 100
    ),
    "Region": np.random.choice(
        ["North", "South", "East", "West", "Central"], 100
    ),
    "Month": np.random.choice(
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 100
    ),
    "SalesAmount": np.random.randint(5000, 50000, 100),
    "UnitsSold": np.random.randint(100, 5000, 100),
    "Target": np.random.randint(4000, 50000, 100),
}

df = pd.DataFrame(data)

# Sidebar Filters
with st.sidebar:
    selected_region = st.selectbox("Select a region:", df["Region"].unique())
    selected_product = st.multiselect("Select products:", df["Product"].unique(), default=df["Product"].unique())

# Apply filters
filtered_df = df[(df["Region"] == selected_region) & (df["Product"].isin(selected_product))]

# KPI Section
with st.container():
    st.subheader(f"Key Performance Indicators for {selected_region}")
    
    total_sales = filtered_df["SalesAmount"].sum()
    total_units = filtered_df["UnitsSold"].sum()
    total_target = filtered_df["Target"].sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Units Sold", f"{total_units:,}")
    col3.metric("Total Target", f"${total_target:,.2f}")

# Break the page into four sections using containers
# First Section: KPIs
with st.container():
    st.subheader(f"Sales Distribution by Product in {selected_region}")
    
    sales_by_product = filtered_df.groupby("Product")["SalesAmount"].sum()
    
    fig1, ax1 = plt.subplots()
    sales_by_product.plot(kind="bar", color="skyblue", ax=ax1)
    ax1.set_title(f"Sales by Product in {selected_region}")
    ax1.set_ylabel("Sales Amount")
    st.pyplot(fig1)

# Second Section: Monthly Sales Trend
with st.container():
    st.subheader(f"Monthly Sales Trend for {selected_region}")
    
    sales_by_month = filtered_df.groupby("Month")["SalesAmount"].sum()
    
    fig2, ax2 = plt.subplots()
    sales_by_month.plot(kind="line", marker="o", color="green", ax=ax2)
    ax2.set_title(f"Monthly Sales in {selected_region}")
    ax2.set_ylabel("Sales Amount")
    st.pyplot(fig2)

# Third Section: Sales Data Table
with st.container():
    st.subheader(f"Sales Data for {selected_region}")
    st.dataframe(filtered_df)

# Footer (Optional)
st.markdown("<br><center><strong>Fintastic Data Solutions - FMCG Sales Analytics</strong></center><br>", unsafe_allow_html=True)
