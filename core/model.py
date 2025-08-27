import os
import chromadb
from openai import OpenAI
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
from tools import get_summary_by_title

# Caches OpenAI and ChromaDB client initialization
_client = None
_collection = None

def load_openai_and_chroma():
    global _client, _collection
    if _client is not None and _collection is not None:
        return _client, _collection

    load_dotenv()
    openai_key = os.getenv("OPENAI_API_KEY")
    _client = OpenAI(api_key=openai_key)

    chroma_client = chromadb.PersistentClient(path="chromadb_data")
    embedding_function = OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-3-small"
    )
    _collection = chroma_client.get_or_create_collection(
        name="books",
        embedding_function=embedding_function
    )

    return _client, _collection

def generate_recommendation(prompt: str, client, collection):
    results = collection.query(query_texts=[prompt], n_results=1)

    if not results["metadatas"][0]:
        return None, None, None

    title = results["metadatas"][0][0]["title"]
    context = results["documents"][0][0]

    gpt_prompt = f"""User asked: \"{prompt}\"

You are a friendly AI librarian. Recommend a book based on the query.
Here is a summary of a matching book:

\"{context}\"

Please recommend the book '{title}' and explain why it's a good match."""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": gpt_prompt}]
    )

    recommendation = completion.choices[0].message.content
    summary = get_summary_by_title(title)

    return title, recommendation, summary