import streamlit as st
import requests
import json

st.title("Medical ChatBot 🇮🇱")

if "phase" not in st.session_state:
    st.session_state.phase = "info_collection"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

user_input = st.text_input("You:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        res = requests.post("http://localhost:8000/chat", json={
            "phase": st.session_state.phase,
            "user_info": st.session_state.user_info,
            "messages": st.session_state.messages
        })
        if res.status_code != 200:
            st.error(f"Error: {res.status_code} - {res.text}")
        else:
            reply = res.json()["response"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.write("Bot:", reply)

            if "confirmed" in reply.lower():
                st.session_state.phase = "qa"
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
