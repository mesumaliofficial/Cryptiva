import streamlit as st
from src.auth.data_handler import load_users, save_users, check_username_exists, hash_password

def style():
    with open("styles/login.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show_sign_up_form():
    with st.form("signup", clear_on_submit=False):
        st.text_input("Username", key="signup_username")
        st.text_input("Email", key="signup_email")
        st.text_input("Password", type="password", key="signup_password")
        st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        submitted = st.form_submit_button("Submit")

        if submitted:
            username = st.session_state.signup_username
            email = st.session_state.signup_email
            password = st.session_state.signup_password
            confirm_password = st.session_state.signup_confirm_password

            hashed_password = hash_password(password)

            if not username or not email or not password or not confirm_password:
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                data = load_users()
                if not check_username_exists(username, email, data):
                    data.append({
                        "username": username,
                        "email": email,
                        "password": hashed_password,
                        "confirm_password": hashed_password
                    })
                    save_users(data)
                    st.success("Sign up successful! You can now log in.")
                else:
                    st.error("Username or email already exists. Please try again with different credentials.")


style()