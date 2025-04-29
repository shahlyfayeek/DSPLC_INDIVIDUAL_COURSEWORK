import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import plotly.express as px

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

# Uncomment to set background image
# set_bg_from_local("bg_image.jpg")

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
    st.markdown("Welcome! This dashboard provides insights into **Sri Lanka’s COVID-19 vaccination campaign** using real data.")

    st.header("🔢 Key Performance Indicators (KPIs)")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💉 Total People Vaccinated", f"{df['people_vaccinated'].max():,.0f}")
    with col2:
        st.metric("📆 Average Daily Vaccinations", f"{df['daily_vaccinations'].mean():,.0f}")
    with col3:
        peak_day = df.loc[df["daily_vaccinations"].idxmax()]["date"].strftime('%Y-%m-%d')
        st.metric("🔝 Peak Vaccination Day", peak_day)

    st.markdown("---")
    st.subheader("📅 Vaccination Timeline")
    start_date = df["date"].min().strftime('%Y-%m-%d')
    end_date = df["date"].max().strftime('%Y-%m-%d')
    st.markdown(f"Data covers the period from **{start_date}** to **{end_date}**.")

    st.subheader("📈 Vaccination Trend")
    fig = px.line(
        df,
        x="date",
        y="daily_vaccinations",
        title="Daily COVID-19 Vaccinations Over Time",
        labels={"daily_vaccinations": "Daily Vaccinations", "date": "Date"},
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🧾 Dataset Preview")
    st.dataframe(df.head())

    if st.checkbox("🔎 Show full dataset"):
        st.dataframe(df)


# ----------------------------
# PAGE: VISUALIZATIONS
# ----------------------------
elif page == "Visualizations":
    st.title("📈 Interactive Visualizations")

    # Metric cards for quick stats
    total_vaccinated = df["people_vaccinated"].max()
    avg_daily_vaccinations = df["daily_vaccinations"].mean()
    peak_vaccination_day = df.loc[df["daily_vaccinations"].idxmax()]["date"]

    st.markdown(f"""
    <div style="display: flex; justify-content: space-around;">
        <div style="background-color: #1E1E1E; padding: 20px; color: white; border-radius: 8px;">
            <h4>Total Vaccinated</h4>
            <p>{total_vaccinated:,.0f}</p>
        </div>
        <div style="background-color: #1E1E1E; padding: 20px; color: white; border-radius: 8px;">
            <h4>Average Daily Vaccinations</h4>
            <p>{avg_daily_vaccinations:,.0f}</p>
        </div>
        <div style="background-color: #1E1E1E; padding: 20px; color: white; border-radius: 8px;">
            <h4>Peak Vaccination Day</h4>
            <p>{peak_vaccination_day}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Interactive plot: Histogram of daily vaccinations
    fig = px.histogram(df, x="daily_vaccinations", nbins=30, title="Distribution of Daily Vaccinations")
    st.plotly_chart(fig)

    # Line chart showing vaccination trends
    selected_column = st.selectbox("Select a column to plot over time", df.columns.tolist())
    fig2 = px.line(df, x="date", y=selected_column, title=f"Vaccination Trends: {selected_column}")
    st.plotly_chart(fig2)

    # Scatter plot: Total vaccinations vs People vaccinated
    fig3 = px.scatter(df, x="people_vaccinated", y="daily_vaccinations", title="Daily Vaccinations vs People Vaccinated")
    st.plotly_chart(fig3)

    # Sidebar filters
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

    # Download button for filtered data
    st.download_button(
        label="Download Filtered Data",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_vaccination_data.csv",
        mime="text/csv"
    )

# ----------------------------
# PAGE: Filters
# ----------------------------
elif page == "Filters":
    st.title("📊 Data Exploration: Filters & Analysis")

    # --- Filter 1: Daily vaccinations threshold ---
    st.subheader("📋 Filter Data by Daily Vaccinations")
    min_input = st.number_input("Set minimum daily vaccinations", min_value=0, value=1000)
    st.dataframe(df[df["daily_vaccinations"] > min_input])

    # ----------------------------
    # 🔹 UNIVARIATE ANALYSIS (Interactive)
    # ----------------------------
    st.subheader("🔹 Univariate Analysis")
    uni_col = st.selectbox("Select a numeric column for distribution analysis", df.select_dtypes('number').columns)
    plot_type = st.radio("Select plot type", ["Histogram", "Boxplot"])

    if plot_type == "Histogram":
        fig = px.histogram(df, x=uni_col, nbins=30, title=f"Distribution of {uni_col}", color_discrete_sequence=["#636EFA"])
    else:  # Boxplot
        fig = px.box(df, x=uni_col, title=f"Boxplot of {uni_col}", color_discrete_sequence=["#EF553B"])
    
    st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # 🔸 BIVARIATE ANALYSIS (Interactive)
    # ----------------------------
    st.subheader("🔸 Bivariate Analysis")
    x_var = st.selectbox("Select X-axis (independent variable)", df.select_dtypes('number').columns, key="x_bivar")
    y_var = st.selectbox("Select Y-axis (dependent variable)", df.select_dtypes('number').columns, key="y_bivar")

    fig2 = px.scatter(
        df, x=x_var, y=y_var, title=f"{y_var} vs {x_var}",
        opacity=0.6, color_discrete_sequence=["#00CC96"],
        labels={x_var: x_var, y_var: y_var}
    )
    st.plotly_chart(fig2, use_container_width=True)

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

