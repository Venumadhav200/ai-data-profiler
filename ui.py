import streamlit as st
from database import create_table, register_user, login_user

create_table()
st.set_page_config(layout="wide")

# 🌈 FULL UI CSS (INSPIRED FROM YOUR DESIGN)
st.markdown("""
<style>

/* Background mesh */
.stApp {
    background: radial-gradient(circle at 20% 20%, #7c3aed33, transparent 40%),
                radial-gradient(circle at 80% 0%, #06b6d433, transparent 40%),
                radial-gradient(circle at 70% 80%, #ec489933, transparent 40%),
                #0f172a;
    color: white;
}

/* Layout */
.container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* LEFT TEXT */
.hero {
    padding: 80px;
}

.hero h1 {
    font-size: 64px;
    font-weight: bold;
    background: linear-gradient(90deg, #22d3ee, #a855f7, #ec4899);
    -webkit-background-clip: text;
    color: transparent;
}

.hero p {
    color: #9ca3af;
    font-size: 18px;
}

/* LOGIN CARD */
.login-card {
    background: rgba(255,255,255,0.05);
    padding: 30px;
    border-radius: 20px;
    width: 350px;
    backdrop-filter: blur(20px);
    box-shadow: 0 0 40px rgba(168,85,247,0.3);
}

/* BUTTON */
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg, #22d3ee, #a855f7, #ec4899);
    color: white;
    border-radius: 12px;
    font-weight: bold;
}

/* INPUT */
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# Layout columns
col1, col2 = st.columns([2,1])

# LEFT SIDE
with col1:
    st.markdown("""
    <div class="hero">
        <h1>Profile your data, instantly.</h1>
        <p>Upload CSV and get insights, quality scores, and analytics in seconds.</p>
    </div>
    """, unsafe_allow_html=True)

# RIGHT SIDE LOGIN
with col2:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    menu = ["Login", "Signup"]
    choice = st.radio("Menu", menu, label_visibility="collapsed")

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            user = login_user(username, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username 
                st.switch_page("pages/main_app.py")
            else:
                st.error("Invalid credentials")

    else:
        st.subheader("Sign Up")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if new_pass != confirm:
                st.error("Passwords do not match")
            else:
                if register_user(new_user, new_pass):
                    st.success("Account created")
                else:
                    st.error("User exists")

    st.markdown('</div>', unsafe_allow_html=True)