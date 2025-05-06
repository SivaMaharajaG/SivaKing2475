import streamlit as st
from db import get_all_users, get_chat_history

st.set_page_config(page_title="Admin Dashboard", layout="wide")
st.title("Admin Dashboard")

if "logged_in" not in st.session_state or not st.session_state.logged_in or st.session_state.role != "admin":
    st.warning("Admin access only.")
    st.stop()

st.subheader("Registered Users")
users = get_all_users()
st.table(users)

st.subheader("Chat History")
selected_user = st.selectbox("Filter by user (or show all)", ["All"] + [u[0] for u in users])

if selected_user == "All":
    chats = get_chat_history()
else:
    chats = get_chat_history(selected_user)

for chat in chats:
    uname, sender, msg, ts = chat
    st.markdown(f"**{uname} ({sender})** [{ts}]: {msg}")
