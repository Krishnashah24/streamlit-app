# app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Page config
st.set_page_config(page_title="Netflix Insights App", layout="wide")
st.title("🎬 Netflix Dataset Insights")
st.markdown("Explore Netflix's content with visual analytics")

# Load dataset
try:
    df = pd.read_csv("netflix_titles.csv")

    st.subheader("📌 Raw Data")
    st.dataframe(df.head())

    st.subheader("🧹 Missing Values")
    st.write(df.isnull().sum())

    # Drop rows with missing values for simplicity
    df_clean = df.dropna()

    st.subheader("📊 Summary Stats")
    st.write(df_clean.describe(include='all'))

    # Correlation (only numerical)
    st.subheader("🔁 Correlation Heatmap")
    if 'release_year' in df_clean:
        corr_df = df_clean[['release_year']]
        fig, ax = plt.subplots()
        sns.heatmap(corr_df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # Time Trend
    if 'date_added' in df_clean:
        df_clean['date_added'] = pd.to_datetime(df_clean['date_added'].str.strip(), format='mixed', errors='coerce')
        df_clean = df_clean.dropna(subset=['date_added'])  # Drop rows where conversion failed
        df_clean['year_added'] = df_clean['date_added'].dt.year
        added_trend = df_clean['year_added'].value_counts().sort_index()
    
        st.subheader("📈 Titles Added Over Years")
        fig2 = px.line(x=added_trend.index, y=added_trend.values,
                   labels={'x': 'Year', 'y': 'Count'})
        st.plotly_chart(fig2, use_container_width=True)


    # Country-wise Top Titles
    st.subheader("🌍 Top Countries")
    country_counts = df_clean['country'].value_counts().head(10)
    fig4 = px.bar(x=country_counts.index, y=country_counts.values,
                  labels={'x': 'Country', 'y': 'Count'})
    st.plotly_chart(fig4, use_container_width=True)

except FileNotFoundError:
    st.error("❌ 'netflix_titles.csv' not found. Please place it in the same folder as this app.")
