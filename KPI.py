import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Data Analytics Platform", layout="wide")

# ------------------------
# UI HEADER
# ------------------------
st.markdown("""
<h1 style='text-align:center; color:#4CAF50;'>📊 Self-Service Data Analytics Platform</h1>
""", unsafe_allow_html=True)

# ------------------------
# FILE UPLOAD
# ------------------------
uploaded_file = st.file_uploader("📂 Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ Data Loaded Successfully")

    # ------------------------
    # BASIC INFO
    # ------------------------
    st.subheader("📌 Dataset Overview")
    st.write(df.head())

    # ------------------------
    # DATA CLEANING
    # ------------------------
    df = df.dropna()

    # ------------------------
    # SIDEBAR FILTERS
    # ------------------------
    st.sidebar.header("🔍 Filters")

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(include='object').columns.tolist()

    # Select columns
    selected_col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)

    # ------------------------
    # KPI SECTION
    # ------------------------
    st.subheader("📊 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Rows", len(df))
    col2.metric("Mean Value", round(df[selected_col].mean(), 2))
    col3.metric("Max Value", df[selected_col].max())

    # ------------------------
    # VISUALIZATION
    # ------------------------
    st.subheader("📈 Data Visualization")

    chart_type = st.selectbox("Select Chart Type", ["Line", "Bar", "Histogram"])

    if chart_type == "Line":
        fig = px.line(df, y=selected_col)
    elif chart_type == "Bar":
        fig = px.bar(df, y=selected_col)
    else:
        fig = px.histogram(df, x=selected_col)

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------
    # CORRELATION HEATMAP
    # ------------------------
    st.subheader("🔥 Correlation Analysis")

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        fig2 = px.imshow(corr, text_auto=True)
        st.plotly_chart(fig2, use_container_width=True)

    # ------------------------
    # INSIGHTS GENERATOR
    # ------------------------
    st.subheader("💡 Insights")

    st.write(f"Average {selected_col} is {round(df[selected_col].mean(),2)}")
    st.write(f"Highest {selected_col} is {df[selected_col].max()}")

else:
    st.info("👆 Upload a CSV file to begin")
