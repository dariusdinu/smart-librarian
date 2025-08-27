import speech_recognition as sr

def record_and_transcribe_google(language="en-US") -> str:
    """
    Records from the default microphone and uses Google's Speech API to transcribe.
    Returns the transcribed text or an empty string on failure.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎙️ Listening... Speak your request.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return ""

    try:
        print("🧠 Transcribing...")
        return recognizer.recognize_google(audio, language=language).strip()
    except sr.UnknownValueError:
        print("😕 Could not understand the audio.")
    except sr.RequestError as e:
        print(f"❌ Google STT request failed: {e}")
    
    return ""
