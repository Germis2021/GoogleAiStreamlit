import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

st.title("Gemini Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
prompt = st.chat_input("Ask something...")

if prompt:
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Format history for Gemini API
        history = [
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages
        ]

        # Start chat with history
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)

        response_text = response.text

    except Exception as e:
        response_text = f"❌ Error: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response_text})

