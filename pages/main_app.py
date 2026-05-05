import streamlit as st
import requests
from database import save_upload
import pandas as pd

# 🔐 Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first")
    st.stop()

# Page config
st.set_page_config(page_title="AI Data Profiler", layout="wide")

# 🎨 FULL UI STYLING
st.markdown("""
<style>

/* 🌈 Background */
.stApp {
    background: radial-gradient(circle at 20% 20%, #7c3aed33, transparent 40%),
                radial-gradient(circle at 80% 0%, #06b6d433, transparent 40%),
                radial-gradient(circle at 70% 80%, #ec489933, transparent 40%),
                #0f172a;
    color: white;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
}

/* Title */
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    background: linear-gradient(90deg, #22d3ee, #a855f7, #ec4899);
    -webkit-background-clip: text;
    color: transparent;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 20px rgba(168,85,247,0.2);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #22d3ee, #a855f7, #ec4899);
    color: white;
    border-radius: 10px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# 🎯 HEADER
st.markdown('<div class="title">AI Data Profiler 🔥</div>', unsafe_allow_html=True)

# 👤 SIDEBAR PROFILE MENU
with st.sidebar:

    st.markdown(f"### 👤 {st.session_state.get('username', 'User')}")
    st.caption("Logged in")

    st.divider()

    with st.expander("⚙️ Menu", expanded=False):

        if st.button("👤 Profile"):
            st.switch_page("pages/profile.py")

        if st.button("⚙️ Settings"):
            st.info("Settings page coming soon")

        if st.button("❓ Help"):
            st.info("Help section coming soon")

        if st.button("🚪 Logout"):
            st.session_state["logged_in"] = False
            st.switch_page("ui.py")

# 📂 Upload section
st.subheader("📂 Upload your dataset")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# 🚀 Analyze
if uploaded_file:
    if st.button("🚀 Analyze Dataset"):
        with st.spinner("Analyzing..."):

            files = {
                "file": (uploaded_file.name, uploaded_file, "text/csv")
            }

            response = requests.post(
                "http://127.0.0.1:8000/analyze/",
                files=files
            )

            if response.status_code == 200:
                save_upload(st.session_state["username"], uploaded_file.name)
                data = response.json()

                st.success("Analysis Complete ✅")
                 # 👋 Welcome message (ADD HERE ✅)
                st.success(f"Welcome {st.session_state['username']} 👋")

                report = data["report"]

                # 🚀 Dataset Overview (ADD HERE ✅)
                st.markdown("### 🚀 Dataset Overview")

                d1, d2, d3 = st.columns(3)

                d1.metric("📄 Rows", report["num_rows"])
                d2.metric("📊 Columns", report["num_columns"])
                d3.metric("🎯 Quality Score", report["data_quality_score"])

                st.divider()
                report = data["report"]

                # 📊 DASHBOARD
                d1, d2, d3 = st.columns(3)
                d1.metric("Rows", report["num_rows"])
                d2.metric("Columns", report["num_columns"])
                d3.metric("Quality", report["data_quality_score"])

                st.divider()

                # 🔥 ADD CHARTS HERE 👇👇👇

                

                # 📉 Missing Values Chart
                st.subheader("📉 Missing Values Analysis")

                missing_df = pd.DataFrame(
                    list(report["missing_values"].items()),
                    columns=["Column", "Missing"]
                )

                st.bar_chart(missing_df.set_index("Column"))

                # 📊 Unique Values Chart
                st.subheader("📊 Unique Value Distribution")

                unique_df = pd.DataFrame(
                    list(report["unique_values"].items()),
                    columns=["Column", "Unique"]
                )

                st.bar_chart(unique_df.set_index("Column"))

                # 📊 HISTOGRAM (from uploaded file)
                uploaded_file.seek(0)   # 🔥 ADD THIS
                df = pd.read_csv(uploaded_file)

                st.subheader("📊 Numeric Distribution")

                numeric_cols = df.select_dtypes(include=['int64', 'float64'])

                for col in numeric_cols.columns:
                    st.write(f"Distribution of {col}")
                    st.bar_chart(df[col].value_counts().head(20))

                st.divider()

                # 📋 EXISTING OUTPUT
                col1, col2 = st.columns(2)

                with col1:
                    st.json(report)

                with col2:
                    st.markdown("### 🧠 AI Summary")
                    st.write(data["summary"])

               