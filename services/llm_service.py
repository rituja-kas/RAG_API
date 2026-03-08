from openai import OpenAI
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


def generate_answer(question: str, context_chunks: list):
    """
    Generate answer using OpenRouter LLM
    """

    if not context_chunks:
        return "No context available to answer the question."

    context_text = "\n\n".join(context_chunks)

    prompt = f"""You are a helpful assistant. Use ONLY the context below to answer the question briefly and accurately.

Context:
{context_text}

Question:
{question}

Answer (be concise):
"""

    try:
        print("⏳ Generating answer with OpenRouter...")
        start_time = time.time()

        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=0.7
        )

        answer = response.choices[0].message.content

        elapsed_time = time.time() - start_time
        print(f"✅ Answer generated in {elapsed_time:.2f} seconds")

        return answer

    except Exception as e:
        print(f"❌ Error in generate_answer: {e}")
        return f"Error generating answer: {str(e)}"