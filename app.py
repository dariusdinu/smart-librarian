import streamlit as st
import chromadb
from openai import OpenAI
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from tools import get_summary_by_title
from better_profanity import profanity
import pyttsx3
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI + ChromaDB
client = OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path="chromadb_data")
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-small")
collection = chroma_client.get_or_create_collection(name="books", embedding_function=embedding_function)

# TTS function (create new engine every time)
def speak(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# UI setup
st.set_page_config(page_title="Smart Librarian", page_icon="📚")
if "gpt_response" not in st.session_state:
    st.session_state.gpt_response = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "title" not in st.session_state:
    st.session_state.title = ""
if "show_output" not in st.session_state:
    st.session_state.show_output = False
st.title("📚 Smart Librarian")
st.markdown("Ask for a book recommendation based on a theme or topic.")

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    generate = st.button("Get Recommendation")

with col2:
    speak_now = st.button("🔊 Read it aloud")

with col3:
    clear = st.button("🧹 Clear")

if clear:
    st.session_state.gpt_response = ""
    st.session_state.summary = ""
    st.session_state.title = ""
    st.session_state.show_output = False
    st.session_state.user_input = ""  # Must happen before rendering the input field
    st.rerun()  # (optional) to fully reset UI

# Input
user_input = st.text_input(
    "Your request", 
    placeholder="e.g. I want a book about friendship and courage.",
    key="user_input"
)

# --- HANDLE LOGIC ---

if generate:
    if profanity.contains_profanity(user_input):
        st.warning("⚠️ Please use respectful language.")
    elif not user_input.strip():
        st.error("Please enter a valid prompt.")
    else:
        results = collection.query(query_texts=[user_input], n_results=1)
        if not results["metadatas"][0]:
            st.info("No matching book found.")
        else:
            title = results["metadatas"][0][0]["title"]
            context = results["documents"][0][0]

            prompt = f"""User asked: "{user_input}"

You are a friendly AI librarian. Recommend a book based on the query.
Here is a summary of a matching book:

"{context}"

Please recommend the book '{title}' and explain why it's a good match."""

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            st.session_state.title = title
            st.session_state.gpt_response = completion.choices[0].message.content
            st.session_state.summary = get_summary_by_title(title)
            st.session_state.show_output = True

# Always show output if available
if st.session_state.get("show_output", False):
    st.subheader("📖 Recommended Book:")
    st.markdown(f"**{st.session_state.title}**")

    st.subheader("🤖 GPT's Recommendation:")
    st.markdown(st.session_state.gpt_response)

    st.subheader("📘 Full Summary:")
    st.markdown(st.session_state.summary)

# Handle TTS button separately
if speak_now and st.session_state.get("show_output", False):
    speak(st.session_state.gpt_response)
    speak(st.session_state.summary)

