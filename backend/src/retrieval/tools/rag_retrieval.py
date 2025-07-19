import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from src.config import settings
from dotenv import load_dotenv

load_dotenv()

def retrieve_similar_chunks(query, top_k=5):
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Encoding query...")
    query_embedding = model.encode([query])[0]

    print("Connecting to Qdrant...")
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
        timeout=60.0
    )

    collection_name = "nephrology_embeddings"

    print(f"Searching for top {top_k} similar chunks...")
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )

    results = []
    for point in search_result:
        results.append({
            "id": point.id,
            "score": point.score,
            "text": point.payload.get("text", "")
        })

    print(f"Found {len(results)} results.")
    return results

if __name__ == "__main__":
    query = input("Enter your search query: ")
    results = retrieve_similar_chunks(query)
    for i, res in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"Score: {res['score']}")
        print(f"Text: {res['text'][:500]}...")  # Show