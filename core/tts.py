import pyttsx3

def speak(text: str, voice_index: int = 0):
    """
    Speaks the given text using a fresh pyttsx3 engine instance.
    This avoids stuck buffers or missing outputs.
    """
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")
    if 0 <= voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()
