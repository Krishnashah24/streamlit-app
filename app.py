# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="📊 CSV Insights App", layout="wide")
st.title("📈 General CSV Insights Explorer")
st.markdown("Upload any CSV file to explore and visualize your data 📂")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Raw Data")
    st.dataframe(df.head())

    st.subheader("🧹 Missing Values")
    st.write(df.isnull().sum())

    # Drop missing values for simplicity
    df_clean = df.dropna()

    st.subheader("📊 Summary Statistics")
    st.write(df_clean.describe(include='all'))

    # Correlation Heatmap
    numeric_cols = df_clean.select_dtypes(include='number')
    if not numeric_cols.empty:
        st.subheader("🔁 Correlation Heatmap (Numeric Columns)")
        fig, ax = plt.subplots()
        sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Date Column Detection
    date_cols = [col for col in df_clean.columns if 'date' in col.lower() or 'time' in col.lower()]
    for date_col in date_cols:
        try:
            df_clean[date_col] = pd.to_datetime(df_clean[date_col].astype(str).str.strip(), errors='coerce', format='mixed')
        except Exception:
            continue

    # Plot Time Trend if any date column found
    for date_col in date_cols:
        if pd.api.types.is_datetime64_any_dtype(df_clean[date_col]):
            df_clean['Year'] = df_clean[date_col].dt.year
            trend = df_clean['Year'].value_counts().sort_index()
            st.subheader(f"📆 Trend Over Time ({date_col})")
            fig2 = px.line(x=trend.index, y=trend.values,
                           labels={'x': 'Year', 'y': 'Count'})
            st.plotly_chart(fig2, use_container_width=True)
            break  # Only show for the first valid datetime column

    # Top Categorical Columns
    st.subheader("🏷️ Top Categorical Feature Counts")
    cat_cols = df_clean.select_dtypes(include='object').columns
    for col in cat_cols[:3]:  # limit to first 3 for simplicity
        top_counts = df_clean[col].value_counts().head(10)
        st.markdown(f"**Top values in `{col}`**")
        fig3 = px.bar(x=top_counts.index, y=top_counts.values,
                      labels={'x': col, 'y': 'Count'})
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Please upload a CSV file to begin.")
