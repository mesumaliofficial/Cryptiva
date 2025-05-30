import streamlit as st
from src.auth.data_handler import load_users, check_credentials, get_user_attempt, update_user_attempt
from datetime import datetime, timedelta


def style():
    with open("styles/login.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_login_form():
    style()

    with st.form("login", clear_on_submit=True):
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")
        
        if submitted:
            username = st.session_state.login_username
            password = st.session_state.login_password
            data = load_users()
            user_attempts = get_user_attempt(username)

            # Check lock time
            if user_attempts["lock_time"]:
                lock_time = datetime.fromisoformat(user_attempts['lock_time'])
                if datetime.now() < lock_time:
                    remaining = (lock_time - datetime.now()).seconds
                    mins, secs = divmod(remaining, 60)
                    st.error(f"🚫 Locked! Try again in {mins}:{secs:02d} minutes.")
                    return

            # Credentials Check
            if check_credentials(username, password, data):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful!")
                update_user_attempt(username, 0, None)  # Reset attempts
                st.rerun()

            else:
                new_attempts = user_attempts['failed_attempts'] + 1
                if new_attempts >= 3:
                    lock_time = (datetime.now() + timedelta(minutes=5)).isoformat()
                    update_user_attempt(username, new_attempts, lock_time)
                    st.error("❌ Too many failed attempts. Locked for 5 minutes.")
                else:
                    update_user_attempt(username, new_attempts, None)
                    st.warning(f"⚠️ Invalid credentials. {3 - new_attempts} attempts left.")
