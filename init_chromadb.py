import json
import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

with open("book_summaries.json", "r") as f:
    books = json.load(f)

chroma_client = chromadb.PersistentClient(path="chromadb_data")

embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-small")

collection = chroma_client.get_or_create_collection(name="books", embedding_function=embedding_function)

for idx, book in enumerate(books):
    collection.add(
        ids=[str(idx)],
        documents=[book["summary"]],
        metadatas=[{"title": book["title"]}]
    )

print("✅ ChromaDB initialized and populated with embeddings.")
