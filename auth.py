import streamlit as st
from db import add_user, authenticate_user, get_user_role

def show_login_page():
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_btn = st.sidebar.button("Login")

    if login_btn:
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = get_user_role(username)
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid credentials")

    st.sidebar.subheader("Register")
    new_user = st.sidebar.text_input("New Username")
    new_pass = st.sidebar.text_input("New Password", type="password")
    role = st.sidebar.selectbox("Role", ["user", "admin"])
    register_btn = st.sidebar.button("Register")

    if register_btn:
        try:
            add_user(new_user, new_pass, role)
            st.success("User registered successfully.")
        except:
            st.error("Username might already exist.")
          
