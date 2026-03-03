import ollama

def generate_answer(question: str, context_chunks: list):

    context_text = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant.
Use ONLY the context below to answer the question.

Context:
{context_text}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="mistral:7b",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]