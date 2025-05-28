import streamlit as st
from src.auth.data_handler import load_users, check_credentials

def style():
    with open("styles/login.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_login_form():
    with st.form("login", clear_on_submit=True):
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            username = st.session_state.login_username
            password = st.session_state.login_password
            data = load_users()
            
            if check_credentials(username, password, data):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

style()