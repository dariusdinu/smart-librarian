import pyttsx3

def speak(text: str, rate: int = 160, voice_index: int = 0):
    """
    Speaks the given text using a fresh pyttsx3 engine instance.
    This avoids stuck buffers or missing outputs.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    voices = engine.getProperty("voices")
    if 0 <= voice_index < len(voices):
        engine.setProperty("voice", voices[voice_index].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()
