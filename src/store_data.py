import streamlit as st
from src.auth.data_handler import hash_password, load_store_data, save_store_data



def render_store_data():

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