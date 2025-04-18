import streamlit as st
import requests
import json

# Set Streamlit page configuration
st.set_page_config(page_title="צ'אטבוט רפואי 🇮🇱", page_icon="💬", layout="centered")

# Language selection
language = st.selectbox("בחר שפה / Choose Language", ("עברית", "English"))

# Set text labels based on selected language
if language == "English":
    page_title = "Medical ChatBot 🇮🇱"
    page_header = "💬 Medical ChatBot 🇮🇱"
    chat_placeholder = "Type your message..."
    bot_typing_text = "Bot is typing..."
    error_prefix = "Error"
    request_failed_text = "Request failed"
    user_text_align = "left"
    user_direction = "ltr"
else:
    page_title = "צ'אטבוט רפואי 🇮🇱"
    page_header = "💬 צ'אטבוט רפואי 🇮🇱"
    chat_placeholder = "כתוב את ההודעה שלך..."
    bot_typing_text = "הבוט מקליד..."
    error_prefix = "שגיאה"
    request_failed_text = "הבקשה נכשלה"
    user_text_align = "right"
    user_direction = "rtl"

# Display the page header
st.markdown(f"""
    <h1 style='text-align: center;'>{page_header}</h1>
""", unsafe_allow_html=True)
st.divider()

# Initialize session state variables
if "phase" not in st.session_state:
    st.session_state.phase = "info_collection"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(
            f"<div style='text-align: {user_text_align}; direction: {user_direction};'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    else:
        st.chat_message("assistant").markdown(
            f"<div style='text-align: {user_text_align}; direction: {user_direction};'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# Input box for user message
user_input = st.chat_input(chat_placeholder)

if user_input:
    st.chat_message("user").markdown(
        f"<div style='text-align: {user_text_align}; direction: {user_direction};'>{user_input}</div>",
        unsafe_allow_html=True
    )
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner(bot_typing_text):
        try:
            res = requests.post(
                "http://localhost:8000/chat",
                json={
                    "phase": st.session_state.phase,
                    "user_info": st.session_state.user_info,
                    "messages": st.session_state.messages
                }
            )

            if res.status_code != 200:
                st.error(f"{error_prefix}: {res.status_code} – {res.text}")
            else:
                data = res.json()
                reply = data["response"]

                st.chat_message("assistant").markdown(
                    f"<div style='text-align: {user_text_align}; direction: {user_direction};'>{reply}</div>",
                    unsafe_allow_html=True
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})

                if "user_info" in data:
                    st.session_state.user_info = data["user_info"]

                if data.get("next_phase") == "qa":
                    st.session_state.phase = "qa"

        except Exception as e:
            st.error(f"{request_failed_text}: {e}")
