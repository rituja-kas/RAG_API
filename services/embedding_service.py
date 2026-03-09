from openai import OpenAI
import os
from dotenv import load_dotenv

# Load .env for local testing
load_dotenv()

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)
print("OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))

def get_embedding(text: str) -> list:
    """
    Get embedding from OpenRouter
    """
    try:
        print(f"Generating embedding for text: {text[:50]}...")
        response = client.embeddings.create(
            model="openai/text-embedding-3-small",
            input=text
        )

        embedding = response.data[0].embedding
        print(f"✅ Generated embedding of length: {len(embedding)}")
        return embedding

    except Exception as e:
        print(f"❌ Error getting embedding: {e}")
        # Return a zero vector as fallback (text-embedding-3-small uses 1536 dimensions)
        return [0.0] * 1536