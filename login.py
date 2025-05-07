import streamlit as st
import pandas as pd

def login_page():
    st.title("Login - Tamil Nadu IT Placement ChatBot")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        df = pd.read_csv("data/users.csv")
        user = df[(df['username'] == username) & (df['password'] == password)]
        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = user.iloc[0]['role']
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
