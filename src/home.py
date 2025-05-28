import streamlit as st
from config.config import LOGO_PATH
import altair as alt
from vega_datasets import data
from src.auth.data_handler import hash_password, load_store_data, save_store_data
import bcrypt

def style():
    with open("styles/home.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_home_page():
    st.sidebar.image(LOGO_PATH, width=180)

    if "current_page" not in st.session_state:
        st.session_state.current_page = 'home'

    if st.sidebar.button("Home", key="home"):
        st.session_state.current_page = "home"

    if st.sidebar.button("Store Data", key="store_data"):
        st.session_state.current_page = "store_data"
    
    if st.sidebar.button("Retrieve Data", key="retrieve_data"):
        st.session_state.current_page = "retrieve_data"

    if st.session_state.current_page == 'home':
        st.session_state.current_page = 'home'
        st.title("🛡️ Secure Data Entry Portal")
        source = data.cars()

        chart = alt.Chart(source).mark_circle().encode(
            x='Horsepower',
            y='Miles_per_Gallon',
            color='Origin',
        ).interactive()

        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    elif st.session_state.current_page == "store_data":
        st.title("📂 Encrypt & Save Your Confidential Data")
        
        with st.form("Store Data", clear_on_submit=False):
            data_name = st.text_input("Enter Your Data Name:", key="data_name")
            data_passkey = st.text_input("Enter Your Passkey / Password:", type="password", key="data_passkey")

            submitted = st.form_submit_button("Encrypt & Save")

        if submitted:
            if not data_name or not data_passkey:
                st.error("Please fill in all fields.")
            else:
                hashed_passkey = hash_password(data_passkey)
                store_data = load_store_data()
                store_data.append({
                    "Data_Name": data_name,
                    "Data_Passkey": hashed_passkey
                })
                save_store_data(store_data)
                st.success("Data encrypted and saved successfully!")
    
    elif st.session_state.current_page == "retrieve_data":
        st.title("🔍 Retrieve Your Encrypted Data")

        with st.form("Retrieve Form", clear_on_submit=False):
            data_name = st.text_input("Enter Your Data Name:")
            data_passkey = st.text_input("Enter Your Passkey:", type="password")

            submitted = st.form_submit_button("Verify & Retrieve")
        
        if submitted:
            store_data = load_store_data()
            matched = False

            for item in store_data:
                if item["Data_Name"] == data_name:
                    stored_hashed_passkey = item['Data_Passkey']
                    if bcrypt.checkpw(data_passkey.encode("utf-8"), stored_hashed_passkey.encode("utf-8")):
                        st.success("✅ Access Granted!")
                        st.info(f"🔐 Your Data Name: **{data_name}**")
                        matched = True
                        break
            if not matched:
                st.error("❌ Invalid data name or passkey.") 
        
    
    style()