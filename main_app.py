import streamlit as st
from database import save_upload
import pandas as pd

# 🔐 Protect page
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please login first")
    st.stop()

# Page config
st.set_page_config(page_title="AI Data Profiler", layout="wide")

# 🎨 UI Styling
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 20% 20%, #7c3aed33, transparent 40%),
                radial-gradient(circle at 80% 0%, #06b6d433, transparent 40%),
                radial-gradient(circle at 70% 80%, #ec489933, transparent 40%),
                #0f172a;
    color: white;
}
.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    background: linear-gradient(90deg, #22d3ee, #a855f7, #ec4899);
    -webkit-background-clip: text;
    color: transparent;
}
</style>
""", unsafe_allow_html=True)

# 🎯 Header
st.markdown('<div class="title">AI Data Profiler 🔥</div>', unsafe_allow_html=True)

# 👤 Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.get('username', 'User')}")
    st.caption("Logged in")

    if st.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.switch_page("ui.py")

# 📂 Upload
st.subheader("📂 Upload your dataset")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# 🚀 Analyze
if uploaded_file:
    if st.button("🚀 Analyze Dataset"):
        with st.spinner("Analyzing..."):

            from profiler import profile_data
            from ai_summary import generate_summary
            import tempfile

            # Save file temporarily
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(uploaded_file.read())
                file_path = tmp.name

            # Process locally
            report = profile_data(file_path)
            summary = generate_summary(report)

            data = {
                "report": report,
                "summary": summary
            }

            # Save upload history
            save_upload(st.session_state["username"], uploaded_file.name)

            # Success messages
            st.success("Analysis Complete ✅")
            st.success(f"Welcome {st.session_state['username']} 👋")

            # 📊 Dataset Overview
            st.markdown("### 🚀 Dataset Overview")

            col1, col2, col3 = st.columns(3)
            col1.metric("📄 Rows", report["num_rows"])
            col2.metric("📊 Columns", report["num_columns"])
            col3.metric("🎯 Quality Score", report["data_quality_score"])

            st.divider()

            # 📉 Missing Values
            st.subheader("📉 Missing Values Analysis")
            missing_df = pd.DataFrame(
                list(report["missing_values"].items()),
                columns=["Column", "Missing"]
            )
            st.bar_chart(missing_df.set_index("Column"))

            # 📊 Unique Values
            st.subheader("📊 Unique Value Distribution")
            unique_df = pd.DataFrame(
                list(report["unique_values"].items()),
                columns=["Column", "Unique"]
            )
            st.bar_chart(unique_df.set_index("Column"))

            # 📊 Numeric Distribution
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)

            st.subheader("📊 Numeric Distribution")

            numeric_cols = df.select_dtypes(include=['int64', 'float64'])

            for col in numeric_cols.columns:
                st.write(f"Distribution of {col}")
                st.bar_chart(df[col].value_counts().head(20))

            st.divider()

            # 📋 Output + AI Summary
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 Report")
                st.json(report)

            with col2:
                st.markdown("### 🧠 AI Summary")
                st.write(summary)