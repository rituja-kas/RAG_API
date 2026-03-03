from pydantic import BaseModel
from typing import Optional, List


class QueryRequest(BaseModel):
    question:str
    top_k:int


class QueryResponse(BaseModel):
    answer:str
    sources:List[str]
