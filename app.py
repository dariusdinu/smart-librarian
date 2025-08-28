import streamlit as st
from core.model import load_openai_and_chroma, generate_recommendation
from core.tts import speak
from core.state import reset_state, initialize_state
from core.image_generation import generate_book_image
from core.stt import record_and_transcribe_google
from tools import get_summary_by_title
from better_profanity import profanity

st.set_page_config(page_title="Smart Librarian", page_icon="📚", layout="centered")

client, collection = load_openai_and_chroma()
initialize_state()

st.title("📚 Smart Librarian")
st.markdown("### Discover books based on your favorite themes and topics!")

# --- Text input
user_input = st.text_input(
    "Type your request below:",
    placeholder="e.g. A book about friendship and bravery",
    key="user_input"
)

# --- Voice input
if st.button("🎙️ Speak", use_container_width=True):
    with st.spinner("🎤 Listening... please speak now"):
        transcription = record_and_transcribe_google()
    if transcription:
        st.session_state.user_input = transcription
        st.toast("✅ Transcription complete!")
    else:
        st.toast("❌ Could not transcribe speech. Try again.")

# --- Get Recommendation button
generate_clicked = st.button("🔍 Get Recommendation", use_container_width=True)

# --- Generate recommendation logic
if generate_clicked:
    if profanity.contains_profanity(user_input):
        st.warning("⚠️ Please use respectful language.")
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
            st.session_state.image_url = ""  # reset image

# --- Display output & buttons if there's valid content
if st.session_state.show_output:
    st.subheader("📖 Recommended Book")
    st.markdown(f"### {st.session_state.title}")

    st.subheader("🧠 GPT's Recommendation")
    st.markdown(f"*{st.session_state.gpt_response}*")

    st.subheader("📘 Full Summary")
    st.markdown(st.session_state.summary)

    # Show post-action buttons
    if st.session_state.show_output:
        col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔊 Read Aloud", use_container_width=True):
            speak(st.session_state.gpt_response)
            speak(st.session_state.summary)
    with col2:
        if st.button("🎨 Generate Cover", use_container_width=True):
            with st.spinner("🎨 Generating AI book cover..."):
                image_url = generate_book_image(st.session_state.title, client)
            if image_url:
                st.session_state.image_url = image_url
                st.toast("🖼️ Cover generated successfully!")
            else:
                st.toast("⚠️ Failed to generate image.")
    with col3:
        if st.button("🧹 Clear", key="clear_final", use_container_width=True):
            reset_state()
            st.rerun()  # ✅ RESTARTS the app with cleared state

    # Show image if it exists
    if st.session_state.get("image_url"):
        st.subheader("🖼️ AI-Generated Book Cover")
        st.image(st.session_state.image_url, use_container_width=True)
