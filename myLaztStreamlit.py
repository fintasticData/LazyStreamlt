import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

# Filter data by region
selected_region = st.sidebar.selectbox("Select a region:", df["Region"].unique())

# Filter data by product
selected_product = st.sidebar.multiselect("Select products:", df["Product"].unique(), default=df["Product"].unique())

# Apply filters
filtered_df = df[(df["Region"] == selected_region) & (df["Product"].isin(selected_product))]

# KPIs Section
st.subheader(f"Key Performance Indicators for {selected_region}")

total_sales = filtered_df["SalesAmount"].sum()
total_units = filtered_df["UnitsSold"].sum()
total_target = filtered_df["Target"].sum()

# Display KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Units Sold", f"{total_units:,}")
col3.metric("Total Target", f"${total_target:,.2f}")

# Sales Chart
st.subheader(f"Sales Distribution by Product in {selected_region}")
sales_by_product = filtered_df.groupby("Product")["SalesAmount"].sum()

fig, ax = plt.subplots()
sales_by_product.plot(kind="bar", color="skyblue", ax=ax)
ax.set_title(f"Sales by Product in {selected_region}")
ax.set_ylabel("Sales Amount")
st.pyplot(fig)

# Monthly Sales Trend
st.subheader(f"Monthly Sales Trend for {selected_region}")
sales_by_month = filtered_df.groupby("Month")["SalesAmount"].sum()

fig, ax = plt.subplots()
sales_by_month.plot(kind="line", marker="o", color="green", ax=ax)
ax.set_title(f"Monthly Sales in {selected_region}")
ax.set_ylabel("Sales Amount")
st.pyplot(fig)

# Show data table
st.subheader(f"Sales Data for {selected_region}")
st.dataframe(filtered_df)

# Footer
st.markdown("**Fintastic Data Solutions - FMCG Sales Analytics**")
