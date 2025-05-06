import streamlit as st
from db import create_user_table, create_chat_table
from auth import show_login_page

create_user_table()
create_chat_table()

st.set_page_config(page_title="Placement ChatBot", layout="centered")
st.title("Welcome to Tamil Nadu IT Placement ChatBot")

show_login_page()
