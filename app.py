import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import time

# ----------------------------
# BACKGROUND IMAGE FUNCTION
# ----------------------------
def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            color: white;
        }}
        .css-1d391kg, .css-1v0mbdj, .css-1cpxqw2, .css-ffhzg2 {{
            color: white !important;
        }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_from_local("bg_image.jpg")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("slcoviddata1.csv", parse_dates=["date"])

df = load_data()

# ----------------------------
# SIDEBAR NAVIGATION
# ----------------------------
st.sidebar.title("📊 Dashboard Menu")
page = st.sidebar.radio("Go to", ["Overview", "Visualizations", "Filters", "About"])

# ----------------------------
# PAGE: OVERVIEW
# ----------------------------
if page == "Overview":
    st.title("🇱🇰 Sri Lanka COVID-19 Vaccination Dashboard")
    st.header("🔍 Explore Vaccination Trends")
    st.markdown("This dashboard provides insights into **Sri Lanka’s COVID-19 vaccination efforts** using an official dataset.")

    st.subheader("📊 Dataset Preview")
    st.caption("Showing the first few rows of the dataset.")
    st.dataframe(df.head())

    if st.checkbox("🔎 Show full dataset"):
        st.dataframe(df)

    if st.button("📈 Show Summary Statistics"):
        st.write(df.describe())

    st.subheader("💻 Code Snippet")
    st.code(
        '''
@st.cache_data
def load_data():
    return pd.read_csv("slcoviddata1.csv", parse_dates=["date"])
        ''',
        language="python"
    )

    st.subheader("📐 Vaccination Rate Formula")
    st.latex(r'''
    \text{Vaccination Rate} = \frac{\text{People Vaccinated}}{\text{Population}} \times 100
    ''')

# ----------------------------
# PAGE: VISUALIZATIONS
# ----------------------------
elif page == "Visualizations":
    st.title("📈 Interactive Visualizations")

    numeric_columns = [
        'people_vaccinated',
        'daily_vaccinations_raw',
        'daily_vaccinations',
        'people_vaccinated_per_hundred',
        'daily_vaccinations_per_million',
        'daily_people_vaccinated',
        'daily_people_vaccinated_per_hundred'
    ]

    selected_radio = st.radio("📉 Select a column to plot over time", numeric_columns)
    st.line_chart(df.set_index("date")[selected_radio])

    selected_iso = st.selectbox("🌍 Filter by ISO Code", df["iso_code"].unique())
    st.dataframe(df[df["iso_code"] == selected_iso])

    selected_cols = st.multiselect("🧩 Choose columns to display", df.columns.tolist())
    if selected_cols:
        st.dataframe(df[selected_cols])

    date_range = st.select_slider(
        "📅 Select date range",
        options=df["date"].dt.strftime('%Y-%m-%d').tolist(),
        value=(df["date"].dt.strftime('%Y-%m-%d').min(), df["date"].dt.strftime('%Y-%m-%d').max())
    )
    st.write(f"Date range selected: {date_range[0]} to {date_range[1]}")
    filtered_df = df[(df["date"] >= date_range[0]) & (df["date"] <= date_range[1])]
    st.line_chart(filtered_df.set_index("date")["daily_vaccinations"])

    threshold = st.slider("📊 Filter: Daily vaccinations above", 0, int(df["daily_vaccinations"].max()), 1000)
    st.dataframe(df[df["daily_vaccinations"] > threshold])

# ----------------------------
# PAGE: Filters
# ----------------------------
elif page == "Filters":
    st.title("🔎 Deep Dive: Data Filtering & Analysis")

    st.markdown("Use the filters below to analyze relationships between key metrics in the COVID-19 vaccination dataset.")

    # Filter by ISO code
    iso_selected = st.selectbox("🌍 Select ISO Country Code", df["iso_code"].unique())
    filtered_df = df[df["iso_code"] == iso_selected]

    # Filter by date range
    date_range = st.slider(
        "📅 Filter by Date Range",
        min_value=df["date"].min().date(),
        max_value=df["date"].max().date(),
        value=(df["date"].min().date(), df["date"].max().date())
    )
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= date_range[0]) & (filtered_df["date"].dt.date <= date_range[1])
    ]

    # Select columns to compare
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    x_col = st.selectbox("📊 Select X-axis (independent variable)", numeric_columns)
    y_col = st.selectbox("📈 Select Y-axis (dependent variable)", numeric_columns)

    st.markdown(f"### 📉 Relationship between `{x_col}` and `{y_col}`")
    fig, ax = plt.subplots()
    ax.scatter(filtered_df[x_col], filtered_df[y_col], alpha=0.6)
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    st.pyplot(fig)

    st.subheader("📄 Filtered Data Preview")
    st.dataframe(filtered_df)


# ----------------------------
# PAGE: ABOUT
# ----------------------------
elif page == "About":
    st.title("ℹ️ About This App")
    st.markdown("""
    This dashboard was created as part of the **5DATA004W Data Science Project Lifecycle** coursework at the University of Westminster.

    **Features:**
    - Visualizes COVID-19 vaccination data for Sri Lanka
    - Provides filters, comparisons, and interactive visuals for data exploration
    - Enables users to investigate trends and relationships over time

    **Developer:** *Shahly Fayeek*  
    **Module Leader:** *Fouzul Hassan*
    """)

    st.subheader("📚 Dataset Field Descriptions")
    st.markdown("""
    - **date**: Date of the observation  
    - **iso_code**: Unique ISO 3166-1 alpha-3 country code  
    - **people_vaccinated**: Cumulative number of individuals who have received at least one vaccine dose  
    - **daily_vaccinations_raw**: Raw number of vaccinations reported on that date (may include backlog)  
    - **daily_vaccinations**: Estimated number of daily vaccinations, cleaned for consistency  
    - **people_vaccinated_per_hundred**: % of the population vaccinated (at least one dose)  
    - **daily_vaccinations_per_million**: Number of vaccinations per one million people per day  
    - **daily_people_vaccinated**: Number of new individuals vaccinated (first dose)  
    - **daily_people_vaccinated_per_hundred**: Daily first-dose vaccinations per 100 people  
    """)



