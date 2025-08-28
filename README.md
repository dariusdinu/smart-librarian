# 📚 Smart Librarian

An AI-powered book recommendation chatbot that suggests titles based on a user's interests, using OpenAI's GPT + ChromaDB (RAG), along with tools for summaries, TTS, STT, and more.

---

## 🚀 Features

- 📖 GPT-powered book recommendation based on user input
- 🧠 Retrieval-Augmented Generation using ChromaDB
- 🗣️ Text-to-speech (offline) using pyttsx3
- 🎙️ Voice input using Google Speech Recognition
- 🖼️ AI-generated book cover (via DALL·E)
- 🧹 Clear UI and state reset
- 🙈 Profanity filter (via better_profanity)
- 🖥️ Streamlit UI and CLI version included

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) for UI
- [OpenAI GPT-3.5](https://platform.openai.com/) for LLM recommendations
- [ChromaDB](https://www.trychroma.com/) for vector similarity search (RAG)
- [pyttsx3](https://pypi.org/project/pyttsx3/) for text-to-speech (offline)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for voice input
- [DALL·E](https://platform.openai.com/docs/guides/images) for image generation

---

## 🛠️ Setup

### 1. Clone the repo
```bash
https://github.com/your-username/smart-librarian.git
cd smart-librarian
```

### 2. Set up your environment
```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

#### Windows:
```bash
setx OPENAI_API_KEY "sk-..."
```

#### Mac/Linux:
```bash
export OPENAI_API_KEY="sk-..."
```

✅ Restart your terminal or IDE afterward.

---

## 💻 Run the App

### Streamlit UI:
```bash
streamlit run app.py
```

### CLI Version:
```bash
python cli_version.py
```

---

## 📷 Screenshots

![screenshot](./assets/screenshot.png) *(Add your screenshot here)*

---

---

## 🧠 Example Prompts
- "I want a book about rebellion and magic"
- "Recommend something that explores freedom and control"
- "Any fantasy with strong female leads?"
