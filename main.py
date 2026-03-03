from fastapi import FastAPI,HTTPException,UploadFile,File
from schemas.query import QueryRequest,QueryResponse
from schemas.chunk import Chunk
from services.chunker import chunktext
from services.embedding_service import get_embedding
from services.retrieval_service import retrieve
from services.llm_service import generate_answer
from storage.memory_store import InMemoryVectorStore
from utils.text_cleaner import  clean_text
app = FastAPI(title="Mini RAG Search API")

vector_store = InMemoryVectorStore()
chunk_id_counter = 0

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    global chunk_id_counter

    if not file.filename:
        raise HTTPException(status_code=400,detail="Only .txt files are supported")

    content = await file.read()
    text = content.decode("utf-8")
    cleaned_text = clean_text(text)

    chunks = chunktext(cleaned_text,chunksize=400,overlap=50)

    for chunk_text_content in chunks:
        embedding = get_embedding(chunk_text_content)
        chunk = Chunk(id=chunk_id_counter,text=chunk_text_content,embedding=embedding)
        vector_store.add(chunk)
        chunk_id_counter += 1

    return {"message":"Document successfully ingested","chunks":len(chunks)}


# query endpoint
@app.post("/query",response_model=QueryResponse)
async def query_document(request:QueryRequest):
    if not vector_store.chunks:
        raise HTTPException(status_code=400,detail="No document ingested yet")

    print("vector_storeeeeeeeeeeeeeee",vector_store)

    retrieved_chunks = retrieve(request.question,vector_store,request.top_k)
    context_texts = [chunk.text for chunk in retrieved_chunks]
    answer = generate_answer(request.question,context_texts)

    return  QueryResponse(answer=answer,sources=context_texts)

@app.get('/health')
async def health():
    return {'status': 'ok'}


