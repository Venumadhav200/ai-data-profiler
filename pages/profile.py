import streamlit as st
from database import update_password
from database import get_user_uploads

# 🔐 Protect page
if "logged_in" not in st.session_state:
    st.warning("Please login first")
    st.stop()

st.title("👤 Profile")

username = st.session_state["username"]

st.write("### Username:")
st.success(username)

st.divider()
st.divider()
st.subheader("📂 Uploaded Files")

uploads = get_user_uploads(username)

if uploads:
    for file in uploads:
        st.write("📄", file[0])
else:
    st.info("No uploads yet")

# 🔐 Update password
new_pass = st.text_input("New Password", type="password")

if st.button("Update Password"):
    if new_pass == "":
        st.warning("Enter a password")
    else:
        update_password(username, new_pass)
        st.success("Password updated successfully 🔐")

# 🔙 Back
if st.button("⬅ Back"):
    st.switch_page("pages/main_app.py")