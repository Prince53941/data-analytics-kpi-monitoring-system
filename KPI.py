import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="KPI Intelligence Dashboard", layout="wide")

st.title("📊 KPI Intelligence & Root Cause Analysis System")

# -------------------------
# Generate Sample Data
# -------------------------
np.random.seed(42)

data = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=200),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 200),
    'product': np.random.choice(['A', 'B', 'C'], 200),
    'revenue': np.random.randint(1000, 5000, 200),
    'orders': np.random.randint(10, 100, 200)
})

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔍 Filters")

selected_region = st.sidebar.multiselect(
    "Select Region", options=data['region'].unique(), default=data['region'].unique()
)

selected_product = st.sidebar.multiselect(
    "Select Product", options=data['product'].unique(), default=data['product'].unique()
)

filtered_data = data[
    (data['region'].isin(selected_region)) &
    (data['product'].isin(selected_product))
]

# -------------------------
# KPI Section
# -------------------------
total_revenue = filtered_data['revenue'].sum()
total_orders = filtered_data['orders'].sum()

col1, col2 = st.columns(2)

col1.metric("💰 Total Revenue", f"{total_revenue:,}")
col2.metric("📦 Total Orders", f"{total_orders:,}")

# -------------------------
# Trend Analysis
# -------------------------
st.subheader("📈 Revenue Trend")

trend = filtered_data.groupby('date')['revenue'].sum().reset_index()

fig = px.line(trend, x='date', y='revenue', title='Revenue Over Time')
st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Revenue Change Detection
# -------------------------
recent = filtered_data.tail(7)['revenue'].sum()
previous = filtered_data.tail(14).head(7)['revenue'].sum()

if previous != 0:
    change = ((recent - previous) / previous) * 100
else:
    change = 0

st.subheader("📉 Revenue Change Analysis")
st.metric("Last 7 Days vs Previous 7 Days", f"{change:.2f}%")

# -------------------------
# Root Cause Analysis
# -------------------------
st.subheader("🔍 Root Cause Analysis")

recent_data = filtered_data.tail(7)
previous_data = filtered_data.tail(14).head(7)

recent_region = recent_data.groupby('region')['revenue'].sum()
previous_region = previous_data.groupby('region')['revenue'].sum()

comparison = pd.DataFrame({
    'recent': recent_region,
    'previous': previous_region
}).fillna(0)

comparison['change_%'] = ((comparison['recent'] - comparison['previous']) / comparison['previous']) * 100
comparison = comparison.replace([np.inf, -np.inf], 0)

st.dataframe(comparison)

# -------------------------
# Visualization
# -------------------------
fig2 = px.bar(comparison.reset_index(), x='region', y='change_%',
              title='Revenue Change % by Region')

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Insight Generator
# -------------------------
st.subheader("💡 Automated Insights")

for index, row in comparison.iterrows():
    if row['change_%'] < 0:
        st.warning(f"⚠️ Revenue decline in {index}: {row['change_%']:.2f}%")
    else:
        st.success(f"✅ Growth in {index}: {row['change_%']:.2f}%")
