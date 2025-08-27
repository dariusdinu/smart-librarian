import json
import os
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()

# Load the .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load book summaries
with open("book_summaries.json", "r") as f:
    books = json.load(f)

# Configure ChromaDB in local mode
chroma_client = chromadb.PersistentClient(path="chromadb_data")

# Set up OpenAI embedding function
embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name="text-embedding-3-small")

# Create a collection
collection = chroma_client.get_or_create_collection(name="books", embedding_function=embedding_function)

# Add book entries
for idx, book in enumerate(books):
    collection.add(
        ids=[str(idx)],
        documents=[book["summary"]],
        metadatas=[{"title": book["title"]}]
    )

print("✅ ChromaDB initialized and populated with embeddings.")

# results = collection.query(
#     query_texts=["I want a book about freedom and government control"],
#     n_results=2
# )

# for match in results["metadatas"][0]:
#     print("📖 Suggested title:", match["title"])
