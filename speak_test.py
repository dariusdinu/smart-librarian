import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

print(f"🔊 Found {len(voices)} voices\n")

for idx, voice in enumerate(voices):
    print(f"🗣️ Voice {idx}: {voice.name} | ID: {voice.id} | Langs: {voice.languages}")
    engine.setProperty('voice', voice.id)
    engine.say(f"This is voice number {idx}. Hello from {voice.name}.")
    engine.runAndWait()