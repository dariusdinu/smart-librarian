import os
import chromadb
from openai import OpenAI
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from tools import get_summary_by_title
from better_profanity import profanity

profanity.load_censor_words()

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

chroma_client = chromadb.PersistentClient(path="chromadb_data")
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-small")
collection = chroma_client.get_or_create_collection(name="books", embedding_function=embedding_function)

print("Welcome to Smart Librarian! Ask for a book. Type 'exit' to quit.")

def contains_profanity(text: str) -> bool:
    return profanity.contains_profanity(text)

while True:
    user_input = input("\nYou: ").strip()

    if contains_profanity(user_input): 
        print("⚠️  Please use adequate language.")
        continue

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye! 👋")
        break

    results = collection.query(query_texts=[user_input], n_results=1)
    if not results["metadatas"][0]:
        print("🤔 Sorry, no matching book found.")
        continue

    top_book = results["metadatas"][0][0]["title"]

    context = results["documents"][0][0]

    prompt = f"""User asked: "{user_input}"

You are a friendly AI librarian. Recommend a book based on the query.
Here is a summary of a matching book:

"{context}"

Please recommend the book '{top_book}' and explain why it's a good match."""
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    print(f"\n🤖 Librarian: {completion.choices[0].message.content}")

    print("\nFull Summary:")
    print(get_summary_by_title(top_book))