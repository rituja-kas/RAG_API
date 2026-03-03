from services.embedding_service import get_embedding

def retrieve(question:str,vector_store:str,top_k:int=3):
    query_embedding = get_embedding(question)
    return vector_store.similarity_search(query_embedding,top_k)
