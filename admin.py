import streamlit as st
import pandas as pd
import json

def admin_page():
    st.title("Admin Dashboard")
    
    st.subheader("User Accounts")
    users = pd.read_csv("data/users.csv")
    st.dataframe(users)

    st.subheader("Chat History")
    with open("data/chat_history.json", "r") as f:
        history = json.load(f)
    st.json(history)
    
