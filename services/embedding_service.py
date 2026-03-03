import ollama



def get_embedding(text):
    response = ollama.embeddings(model="mistral:7b")
    embedding_vector = response["embedding"]
    return response["embedding"]