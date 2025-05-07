import streamlit as st
from utils import get_relevant_chunk, ask_bot, save_chat
import datetime

def user_page():
    st.title("Placement ChatBot - User")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask about placements based on your qualification")

    if user_input:
        chunk = get_relevant_chunk(user_input)
        bot_response = ask_bot(user_input, chunk)
        st.session_state.chat_history.append((user_input, bot_response))
        save_chat(st.session_state.username, user_input, bot_response)

    for q, r in st.session_state.chat_history:
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Bot:** {r}")
