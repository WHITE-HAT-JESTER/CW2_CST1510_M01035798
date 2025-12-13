import streamlit as st
from google import genai

from genai import messages

client=genai.Client(api=st.secrets["GEMINI_API_KEY"])
st.subheader("Gemini API")

#Initialise session state
if 'messages' not in st.session_state.messages:
    if messages:

    #Display
    for message in st.session_state.messages:
        if message["role"] == "model":
            role = "assistant"
        else:
            role = message["role"]
        with st.chat_message(role):
            st.markdown(message["parts"][0]["text"])
#prompt st.chat_input("say something")

#if prompt:

    #with st.chat_message(prompt):
