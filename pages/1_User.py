import streamlit as st
from chatbot import get_bot_response
from db import log_chat
from datetime import datetime

st.set_page_config(page_title="Placement Chat - User", layout="centered")
st.title("Placement ChatBot (Tamil Nadu)")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login to access the chat.")
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

with st.expander("Optional Filters", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        qualification = st.selectbox("Your Qualification", ["", "B.E", "MCA", "B.Sc", "Diploma"])
    with col2:
        location = st.selectbox("Preferred Location", ["", "Chennai", "Coimbatore", "Madurai", "Salem", "Tirunelveli"])

query = st.text_input("Ask a question about placements:", placeholder="e.g., Placement availability for B.E graduates in Chennai")

if st.button("Send") and query:
    context = ""
    if qualification:
        context += f"My qualification is {qualification}. "
    if location:
        context += f"I am looking for jobs in {location}. "
    final_query = context + query

    bot_response = get_bot_response(final_query)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chat_history.append(("You", query, timestamp))
    st.session_state.chat_history.append(("Bot", bot_response, timestamp))

    log_chat(st.session_state.username, st.session_state.role, query, "user")
    log_chat(st.session_state.username, st.session_state.role, bot_response, "bot")
    st.experimental_rerun()

st.subheader("Chat History")
for speaker, message, timestamp in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 {st.session_state.username}** ({timestamp}): {message}")
    else:
        st.markdown(f"**🤖 Bot** ({timestamp}): {message}")
