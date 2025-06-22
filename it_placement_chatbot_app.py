# it_placement_chatbot_app.py

import streamlit as st
import sqlite3
from datetime import datetime
from webbrowser import open as open_web
from chatbot_utils import get_relevant_chunks, query_web, generate_response
from file_utils import extract_text_from_pdf, chunk_text

# Database setup
def create_tables():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    qualification TEXT,
                    role TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    query TEXT,
                    response TEXT,
                    timestamp TEXT
                )''')
    conn.commit()
    conn.close()

# Login & Signup

def signup():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    qualification = st.text_input("Qualification")
    if st.button("Register"):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, qualification, role) VALUES (?, ?, ?, ?)",
                      (username, password, qualification, 'user'))
            conn.commit()
            st.success("Registered successfully. Please login.")
        except:
            st.error("Username already exists.")
        conn.close()

def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        if result:
            st.session_state['user_id'] = result[0]
            st.session_state['role'] = result[1]
            st.session_state['username'] = username
            st.success("Login successful")
        else:
            st.error("Invalid credentials")
        conn.close()

# Chat Page

def user_chat():
    st.title("Placement Chatbot")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    query = st.text_input("Ask about IT placements in Tamil Nadu")
    if st.button("Submit"):
        chunks = get_relevant_chunks(query)
        web_data = query_web(query)
        response = generate_response(query, chunks, web_data)

        st.markdown(f"**You:** {query}")
        st.markdown(f"**Bot:** {response}")

        st.session_state.chat_history.append((query, response))
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO history (user_id, query, response, timestamp) VALUES (?, ?, ?, ?)",
                  (st.session_state['user_id'], query, response, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    st.markdown("### Chat History")
    for q, r in st.session_state['chat_history']:
        st.markdown(f"**Q:** {q}")
        st.markdown(f"**A:** {r}")

# Admin Page

def admin_dashboard():
    st.title("Admin Dashboard")
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT username, qualification, role FROM users")
    users = c.fetchall()
    st.markdown("### Registered Users")
    for u in users:
        st.markdown(f"**Username:** {u[0]} | **Qualification:** {u[1]} | **Role:** {u[2]}")
    conn.close()

    st.markdown("### Upload Company PDF Info")
    pdf_file = st.file_uploader("Upload Company Placement PDF", type=['pdf'])
    if pdf_file:
        text = extract_text_from_pdf(pdf_file)
        chunks = chunk_text(text)
        st.session_state['uploaded_chunks'] = chunks
        st.success(f"Uploaded and chunked {len(chunks)} segments.")

# Profile Edit

def profile():
    st.title("Edit Profile")
    new_qualification = st.text_input("Update Qualification")
    if st.button("Update"):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("UPDATE users SET qualification=? WHERE id=?", (new_qualification, st.session_state['user_id']))
        conn.commit()
        conn.close()
        st.success("Profile updated")

    st.markdown("### Upload Resume")
    resume = st.file_uploader("Upload your resume (PDF)", type=['pdf'])
    if resume:
        resume_text = extract_text_from_pdf(resume)
        st.success("Resume uploaded and read successfully.")
        st.text_area("Resume Text", resume_text[:1000], height=200)

# Main

def main():
    create_tables()
    if 'user_id' not in st.session_state:
        menu = st.sidebar.radio("Menu", ["Login", "Sign Up"])
        if menu == "Login":
            login()
        else:
            signup()
    else:
        menu = st.sidebar.radio("Navigation", ["Chat", "Profile", "Logout"] if st.session_state['role'] == 'user' else ["Admin", "Logout"])
        if menu == "Chat":
            user_chat()
        elif menu == "Profile":
            profile()
        elif menu == "Admin":
            admin_dashboard()
        elif menu == "Logout":
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            return st.experimental_rerun()

if __name__ == '__main__':
    main()
