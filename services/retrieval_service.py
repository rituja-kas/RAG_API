# services/retrieval_service.py
from services.embedding_service import get_embedding


def retrieve(question: str, vector_store, top_k: int = 3):
    """
    Retrieve relevant chunks for a question
    """
    print(f"Retrieving for question: {question}")  # Debug print

    # Get embedding for the question
    query_embedding = get_embedding(question)
    print(f"Query embedding generated, length: {len(query_embedding)}")

    # Check if vector store has chunks
    print(f"Vector store has {len(vector_store.chunks)} chunks")

    # Use the similarity_search method
    relevant_chunks = vector_store.similarity_search(query_embedding, top_k)

    print(f"Retrieved {len(relevant_chunks)} chunks")
    return relevant_chunks