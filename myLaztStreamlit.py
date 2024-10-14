import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the page layout to wide for better utilization of screen space
st.set_page_config(layout="wide")

# Setting the title of the dashboard
st.markdown("""
    <h1 style='text-align: center; color: #D32F2F;'>FMCG Sales Dashboard</h1>
""", unsafe_allow_html=True)

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
    st.markdown("""
        <h3 style='color: #333333;'>Filters</h3>
    """, unsafe_allow_html=True)
    selected_region = st.selectbox("Select a region:", df["Region"].unique())
    selected_product = st.multiselect(
        "Select products:", df["Product"].unique(), default=[df["Product"].unique()[0]]
    )

# Apply filters
filtered_df = df[(df["Region"] == selected_region) & (df["Product"].isin(selected_product))]

# Tabs Section
tab1, tab2, tab3, tab4 = st.tabs(["KPI Overview", "Sales Distribution", "Monthly Trend", "Sales Data"])

# KPI Section
with tab1:
    st.markdown(f"<h2 style='color: #D32F2F;'>Key Performance Indicators for {selected_region}</h2>", unsafe_allow_html=True)
    
    total_sales = filtered_df["SalesAmount"].sum()
    total_units = filtered_df["UnitsSold"].sum()
    total_target = filtered_df["Target"].sum()
    
    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Total Sales", f"${total_sales:,.2f}", delta_color="inverse")
    col2.metric("Total Units Sold", f"{total_units:,}", delta_color="inverse")
    col3.metric("Total Target", f"${total_target:,.2f}", delta_color="inverse")

# Sales Distribution by Product
with tab2:
    st.markdown(f"<h2 style='color: #D32F2F;'>Sales Distribution by Product in {selected_region}</h2>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        sales_by_product = filtered_df.groupby("Product")["SalesAmount"].sum()

        fig1, ax1 = plt.subplots(figsize=(10, 4))
        sales_by_product.plot(kind="bar", color="#D32F2F", ax=ax1)
        ax1.set_title(f"Sales by Product in {selected_region}", fontsize=16, color="black")
        ax1.set_ylabel("Sales Amount", fontsize=12, color="black")
        ax1.tick_params(axis='x', labelsize=10, colors="black")
        ax1.tick_params(axis='y', labelsize=10, colors="black")
        st.pyplot(fig1)
    else:
        st.write("No data available for the selected filters.")

# Monthly Sales Trend
with tab3:
    st.markdown(f"<h2 style='color: #D32F2F;'>Monthly Sales Trend for {selected_region}</h2>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        sales_by_month = filtered_df.groupby("Month")["SalesAmount"].sum()
        sales_by_month = sales_by_month.reindex(
            ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        )

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        sales_by_month.plot(kind="line", marker="o", color="#607D8B", ax=ax2)
        ax2.set_title(f"Monthly Sales in {selected_region}", fontsize=16, color="black")
        ax2.set_ylabel("Sales Amount", fontsize=12, color="black")
        ax2.tick_params(axis='x', labelsize=10, colors="black")
        ax2.tick_params(axis='y', labelsize=10, colors="black")
        st.pyplot(fig2)
    else:
        st.write("No data available for the selected filters.")

# Sales Data Table
with tab4:
    st.markdown(f"<h2 style='color: #D32F2F;'>Sales Data for {selected_region}</h2>", unsafe_allow_html=True)
    st.dataframe(filtered_df, width=1000, height=500)

# Footer (Optional)
st.markdown("<br><center><strong style='color: #333333;'>Powered by Fintastic Data Solutions &copy; 2024</strong></center><br>", unsafe_allow_html=True)
