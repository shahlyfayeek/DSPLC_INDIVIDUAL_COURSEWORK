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
page = st.sidebar.radio("Go to", ["Overview", "Visualizations", "UI Elements Demo", "About"])

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
# PAGE: UI ELEMENTS DEMO
# ----------------------------
elif page == "UI Elements Demo":
    st.title("🧪 Streamlit UI Elements Showcase")

    if st.button("🎈 Celebrate with Balloons"):
        st.balloons()

    st.subheader("🔄 Simulated Progress Bar")
    progress_bar = st.progress(0)
    for percent in range(0, 101, 10):
        time.sleep(0.05)
        progress_bar.progress(percent)

    st.subheader("⏳ Simulated Loading Spinner")
    with st.spinner("Loading health data..."):
        time.sleep(1)
    st.success("Data loaded successfully!")

    min_input = st.number_input("👨‍⚕️ Set minimum daily vaccinations", min_value=0, value=1000)
    st.write(df[df["daily_vaccinations"] > min_input])

    name = st.text_input("📝 Your name")
    if name:
        st.success(f"Welcome, {name}!")

    chosen_date = st.date_input("📆 Choose a date")
    st.write(f"You picked: {chosen_date}")

    chosen_time = st.time_input("⏰ Choose a time")
    st.write(f"You picked: {chosen_time}")

    feedback = st.text_area("💬 Feedback")
    if feedback:
        st.info("Thanks for your input!")

    uploaded = st.file_uploader("📂 Upload a CSV file", type=["csv"])
    if uploaded is not None:
        try:
            user_df = pd.read_csv(uploaded)
            st.success("File uploaded successfully.")
            st.dataframe(user_df.head())
        except Exception as e:
            st.error(f"Failed to load file: {e}")

    bg_color = st.color_picker("🎨 Pick a dashboard color", "#00f900")
    st.write(f"Selected color: {bg_color}")

# ----------------------------
# PAGE: ABOUT
# ----------------------------
elif page == "About":
    st.title("ℹ️ About This App")
    st.markdown("""
    This dashboard was created as part of the **5DATA004W Data Science Project Lifecycle** coursework at the University of Westminster.

    **Features:**
    - Visualizes COVID-19 vaccination data for Sri Lanka
    - Interactive widgets powered by Streamlit
    - Full use of UI components, file uploaders, filters, and more

    **Developer:** *Shahly Fayeek*  
    **Module Leader:** *Fouzul Hassan*  
    """)

    st.subheader("📤 Background Image Uploader (Optional)")
    st.info("You can replace `mybg.jpg` in your project folder with another image to customize the look!")

