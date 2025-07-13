import os
import time
from sentence_transformers import SentenceTransformer
from ingestion.chunking import chunk_pdf
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from dotenv import load_dotenv

load_dotenv()

def upload_in_batches(client, collection_name, points, batch_size=500):
    total = len(points)
    for i in range(0, total, batch_size):
        batch = points[i:i + batch_size]
        attempt = 1
        while attempt <= 3:
            try:
                print(f"Uploading batch {i + 1} to {i + len(batch)} (Attempt {attempt})...")
                client.upsert(collection_name=collection_name, points=batch)
                break  # success
            except Exception as e:
                print(f"Error uploading batch {i + 1}–{i + len(batch)}: {e}")
                if attempt < 3:
                    print("Retrying in 5 seconds...")
                    time.sleep(5)
                    attempt += 1
                else:
                    print("Failed after 3 attempts. Exiting.")
                    raise


def process_pdf_embeddings(pdf_path):
    print("Starting PDF chunking...")
    chunks = chunk_pdf(pdf_path)
    print(f"Chunking complete. Number of chunks: {len(chunks)}")

    print("Extracting text from chunks...")
    texts = [chunk.page_content for chunk in chunks]
    print(f"Text extraction complete. Number of texts: {len(texts)}")

    print("Loading Hugging Face embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded.")

    print("Generating embeddings for each chunk...")
    embeddings = model.encode(texts)
    print(f"Generated {len(embeddings)} embeddings.")
    print(f"First embedding vector (truncated): {embeddings[0][:10]}")

    # --- Qdrant Vector Store Integration ---
    print("Connecting to Qdrant...")
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=60.0  # increase timeout
    )

    collection_name = "nephrology_embeddings"
    vector_size = len(embeddings[0])

    try:
        print("Creating new Qdrant collection...")
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        print(f"Collection '{collection_name}' created.")

        print("Preparing points for upload...")
        points = [
            PointStruct(id=i, vector=embeddings[i], payload={"text": texts[i]})
            for i in range(len(embeddings))
        ]

        print("Uploading vectors to Qdrant in batches...")
        upload_in_batches(client, collection_name, points, batch_size=500)
        print(f"All {len(points)} vectors uploaded to Qdrant collection '{collection_name}'.")

    except Exception as e:
        print(f"Failed to upload vectors to Qdrant: {e}")
        raise

    print("Embedding process completed successfully.")
    return len(chunks), len(embeddings)


if __name__ == "__main__":
    pdf_path = input("Enter the path to the PDF file: ")
    process_pdf_embeddings(pdf_path)
