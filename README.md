Mini RAG Search API

A beginner-friendly Retrieval-Augmented Generation (RAG) system built using FastAPI and Ollama.

This project demonstrates the fundamentals of:
Text chunking.
Embedding generation.
Vector similarity search (cosine similarity).
Prompt engineering.
Clean API Design.

Features
Upload .txt document (max 1MB)
Automatic chunking (300–500 characters)
Embedding generation using Ollama
In-memory vector storage
Cosine similarity retrieval
Context-aware answer generation
Interactive Swagger UI testing

System Architecture
User → FastAPI → Chunker → Embedding Service → Memory Store
User → FastAPI → Retrieval → Similarity Search → LLM → Response

Folder Structure
mini_rag_api/
│
├── main.py
├── schemas/
│   ├── ingest.py
│   └── query.py
├── services/
│   ├── chunker.py
│   ├── embedding_service.py
│   ├── retrieval_service.py
│   └── llm_service.py
├── storage/
│   └── memory_store.py
├── utils/
│   └── text_cleaner.py
├── README.md

Setup Instruction and run the project.
1.Clone the repository. 
2.Create the virtual environment by using -"python -m venv venv"
3.pip install fastapi uvicorn python-multipart numpy ollama python-dotenv
4.ollama pull mistral:7b
5.Start the fastapi server:uvicorn main:app --reload 
6.Open swagger UI to check the API's working:http://127.0.0.1:8000/docs

API endpoint
1.upload document api endpoint-http://127.0.0.1:8000/ingest
2.query api endpoint-http://127.0.0.1:8000/query
3.health api endpoint-http://127.0.0.1:8000/health

Example 1. Request for uploading document we need to upload the .txt file and it will response like
{
  "message": "Document ingested successfully",
  "chunks": 42
}
Example 2. we need to put the question and top_k as an integer in the parameter and it will response like below
{
  "question": "What is Retrieval-Augmented Generation?",
  "top_k": 3
}
then it will generate the more relatable response by similar search
Example 3. No parameter required for health api it is quietly to check the response only as per below.
{
  "status": "ok"
}

This is final repo