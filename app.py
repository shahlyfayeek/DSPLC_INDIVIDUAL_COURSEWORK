import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("slcoviddata1.csv")

df = load_data()

# App layout
st.title("Coronavirus (COVID-19) Vaccinations")
st.markdown("This dashboard provides insights for policymakers.")

# Sidebar filters
selected_column = st.sidebar.selectbox("Choose a column to explore", df.columns)

# Display data
st.write("## Dataset Preview")
st.dataframe(df)

# Visualization
st.write("## Distribution Plot")
fig = px.histogram(df, x=selected_column)
st.plotly_chart(fig)

# Optional: More interactive charts, insights, summaries, etc.
