from core.model import load_openai_and_chroma, generate_recommendation
from core.tts import speak
from better_profanity import profanity

profanity.load_censor_words()

client, collection = load_openai_and_chroma()

print("Welcome to Smart Librarian (CLI Version)!\n")
print("Ask for a book. Type 'exit' or 'quit' to terminate.")

def main():
    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        if profanity.contains_profanity(user_input):
            print("⚠️  Please use adequate language.")
            continue

        title, recommendation, summary = generate_recommendation(user_input, client, collection)

        if title is None:
            print("🤔 Sorry, no matching book found.")
            continue

        print(f"\n🤖 Librarian recommends: {title}\n")
        print(recommendation)
        speak(recommendation)

        print("\n📘 Full Summary:")
        print(summary)
        speak(summary)

if __name__ == "__main__":
    main()
