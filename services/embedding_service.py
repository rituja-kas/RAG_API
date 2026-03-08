# services/embedding_service.py
import ollama
import numpy as np


def get_embedding(text: str) -> list:
    """
    Get embedding from Ollama using nomic-embed-text
    """
    try:
        print(f"Generating embedding for text: {text[:50]}...")
        response = ollama.embeddings(
            model="nomic-embed-text",  # You already have this
            prompt=text
        )

        embedding = response["embedding"]
        print(f"✅ Generated embedding of length: {len(embedding)}")
        return embedding

    except Exception as e:
        print(f"❌ Error getting embedding: {e}")
        # Return a zero vector as fallback (nomic-embed-text uses 384 dimensions)
        return [0.0] * 384