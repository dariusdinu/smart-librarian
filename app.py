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

if st.button("🎙️ Speak"):
    with st.spinner("🎤 Listening... please speak now"):
        transcription = record_and_transcribe_google()
    if transcription:
        st.session_state.user_input = transcription
        st.toast("✅ Transcription complete!")
    else:
        st.toast("❌ Could not transcribe speech. Try again.")

user_input = st.text_input(
    "Type your request below:",
    placeholder="e.g. A book about friendship and bravery",
    key="user_input"
)

generate_clicked = st.button("🔍 Get Recommendation", use_container_width=True)

speak_clicked = False
image_clicked = False
clear_clicked = False


# Show post-action buttons only if output is visible
if st.session_state.show_output:
    st.markdown("### What would you like to do next?")
    secondary_cols = st.columns([1, 1, 1])
    with secondary_cols[0]:
        speak_clicked = st.button("🔊 Read Aloud", use_container_width=True)    
    with secondary_cols[1]:
        image_clicked = st.button("🎨 Generate Cover", use_container_width=True)    
    with secondary_cols[2]:
        clear_clicked = st.button("🧹 Clear", use_container_width=True) 
else:
    # Show Clear button in initial state too
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    if st.button("🧹 Clear", use_container_width=True):
        reset_state()


if clear_clicked:
    reset_state()

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

if speak_clicked and st.session_state.show_output:
    speak(st.session_state.gpt_response)
    speak(st.session_state.summary)

if image_clicked and st.session_state.show_output:
    with st.spinner("🎨 Generating AI book cover..."):
        image_url = generate_book_image(st.session_state.title, client)
    if image_url:
        st.session_state.image_url = image_url
        st.toast("🖼️ Cover generated successfully!")
    else:
        st.toast("⚠️ Failed to generate image.")

# Output display
if st.session_state.show_output:
    st.subheader("📖 Recommended Book")
    st.markdown(f"### {st.session_state.title}")

    st.subheader("🧠 GPT's Recommendation")
    st.markdown(f"*{st.session_state.gpt_response}*")

    st.subheader("📘 Full Summary")
    st.markdown(st.session_state.summary)

    if st.session_state.get("image_url"):
        st.subheader("🖼️ AI-Generated Book Cover")
        st.image(st.session_state.image_url, use_container_width=True)