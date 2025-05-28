import streamlit as st
from src.auth.login import show_login_form
from src.auth.sign_up import show_sign_up_form
from config.config import LOGO_PATH
from src.home import render_home_page

def style():
    with open("styles/login.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def initialize_session_state():
    defaults = {
        'logged_in': False,
        'username': None,
        'show_sign_up': False,
        'show_login': False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

if st.session_state.logged_in:  
    render_home_page()

else:
    st.image(LOGO_PATH, width=200)
    st.subheader("World No: 1 Secure System for your data")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state.show_login = True
            st.session_state.show_sign_up = False
    with col2:
        if st.button("Sign Up"):
            st.session_state.show_sign_up = True
            st.session_state.show_login = False

    if st.session_state.show_sign_up:
        show_sign_up_form()
    else:
        show_login_form()

    style()