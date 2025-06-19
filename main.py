import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Įkeliame .env failą
load_dotenv()

# Konfigūruojame Google API raktą
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Inicijuojame Gemini modelį
modelis = genai.GenerativeModel('gemini-pro')

st.title("Gemini Pokalbių Botas")

# Chat istorija sesijoje
if "messages" not in st.session_state:
    st.session_state.messages = []

# Atvaizduojame senas žinutes
for zinute in st.session_state.messages:
    with st.chat_message(zinute["role"]):
        st.markdown(zinute["content"])

# Įvestis iš naudotojo
prompt = st.chat_input("Paklausk ko nors...")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Gemini istorija (role: user / model)
        istorija = [
            {"role": m["role"], "parts": [m["content"]]}
            for m in st.session_state.messages
        ]

        chat = modelis.start_chat(history=istorija)
        atsakymas = chat.send_message(prompt)

        atsakymo_tekstas = atsakymas.text

    except Exception as klaida:
        atsakymo_tekstas = f"❌ Klaida: {klaida}"

    with st.chat_message("assistant"):
        st.markdown(atsakymo_tekstas)

    st.session_state.messages.append({"role": "assistant", "content": atsakymo_tekstas})
