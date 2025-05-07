import streamlit as st
from login import login_page
from user import user_page
from admin import admin_page

# Hide Streamlit's sidebar completely for login
st.set_page_config(page_title="Placement ChatBot", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_page()
else:
    role = st.session_state.get("role")
    if role == "user":
        user_page()
    elif role == "admin":
        admin_page()

