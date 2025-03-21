# streamlit_app.py

import streamlit as st
import requests

st.title("Callisto Voice Assistant")

if st.button("Speak to Callisto (Live)"):
    with st.spinner("Listening..."):
        try:
            response = requests.post("http://localhost:8000/live-voice-query/")
            response.raise_for_status()
            result = response.json()
            st.write(f"User said: {result['user_input']}")
            st.write(f"Callisto says: {result['response']}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")

if st.button("Process Recorded Audio"):
    with st.spinner("Processing..."):
        try:
            response = requests.post("http://localhost:8000/voice-query/")
            response.raise_for_status()
            result = response.json()
            st.write(f"User said: {result['user_input']}")
            st.write(f"Callisto says: {result['response']}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error: {e}")