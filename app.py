import streamlit as st
from core.model import load_openai_and_chroma, generate_recommendation
from core.tts import speak
from core.state import reset_state, initialize_state
from better_profanity import profanity

# Set up the page
st.set_page_config(page_title="Smart Librarian", page_icon="📚")

# Load clients (cached)
client, collection = load_openai_and_chroma()

# Initialize session state
initialize_state()

# --- Clear button logic (first)
if st.button("🧹 Clear"):
    reset_state()

# --- Input box
user_input = st.text_input(
    "Your request",
    placeholder="e.g. A book about friendship and bravery",
    key="user_input"
)

# --- Buttons
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Get Recommendation"):
        if profanity.contains_profanity(user_input):
            st.warning("\u26a0\ufe0f Please use respectful language.")
        elif not user_input.strip():
            st.error("Please enter a valid prompt.")
        else:
            title, gpt_response, summary = generate_recommendation(user_input, client, collection)
            if title is None:
                st.info("No matching book found.")
            else:
                st.session_state.title = title
                st.session_state.gpt_response = gpt_response
                st.session_state.summary = summary
                st.session_state.show_output = True

with col2:
    if st.button("\ud83c\udfa7 Read it aloud") and st.session_state.show_output:
        speak(st.session_state.gpt_response)
        speak(st.session_state.summary)

# --- Display output
if st.session_state.show_output:
    st.subheader("\ud83d\udcd6 Recommended Book:")
    st.markdown(f"**{st.session_state.title}**")

    st.subheader("\ud83e\udde0 GPT's Recommendation:")
    st.markdown(st.session_state.gpt_response)

    st.subheader("\ud83d\udcd8 Full Summary:")
    st.markdown(st.session_state.summary)
