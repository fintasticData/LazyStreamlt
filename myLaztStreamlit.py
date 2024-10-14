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
    selected_product = st.multiselect(
        "Select products:", df["Product"].unique(), default=[df["Product"].unique()[0]]
    )

# Apply filters
filtered_df = df[(df["Region"] == selected_region) & (df["Product"].isin(selected_product))]

# KPI Section
with st.container():
    st.subheader(f"Key Performance Indicators for {selected_region}")
    
    total_sales = filtered_df["SalesAmount"].sum()
    total_units = filtered_df["UnitsSold"].sum()
    total_target = filtered_df["Target"].sum()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Units Sold", f"{total_units:,}")
    col3.metric("Total Target", f"${total_target:,.2f}")

# Adding a separator for better visual distinction
st.markdown("---")

# Sales Distribution by Product
with st.container():
    st.subheader(f"Sales Distribution by Product in {selected_region}")
    
    if not filtered_df.empty:
        sales_by_product = filtered_df.groupby("Product")["SalesAmount"].sum()

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        sales_by_product.plot(kind="bar", color="#1f77b4", ax=ax1)
        ax1.set_title(f"Sales by Product in {selected_region}", fontsize=16)
        ax1.set_ylabel("Sales Amount", fontsize=12)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        st.pyplot(fig1)
    else:
        st.write("No data available for the selected filters.")

# Adding a separator for better visual distinction
st.markdown("---")

# Monthly Sales Trend
with st.container():
    st.subheader(f"Monthly Sales Trend for {selected_region}")
    
    if not filtered_df.empty:
        sales_by_month = filtered_df.groupby("Month")["SalesAmount"].sum()
        sales_by_month = sales_by_month.reindex(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        )

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sales_by_month.plot(kind="line", marker="o", color="green", ax=ax2)
        ax2.set_title(f"Monthly Sales in {selected_region}", fontsize=16)
        ax2.set_ylabel("Sales Amount", fontsize=12)
        ax2.tick_params(axis='x', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        st.pyplot(fig2)
    else:
        st.write("No data available for the selected filters.")

# Adding a separator for better visual distinction
st.markdown("---")

# Sales Data Table
with st.container():
    st.subheader(f"Sales Data for {selected_region}")
    st.dataframe(filtered_df)

# Footer (Optional)
st.markdown("<br><center><strong>Powered by Fintastic Data Solutions &copy; 2024</strong></center><br>", unsafe_allow_html=True)
