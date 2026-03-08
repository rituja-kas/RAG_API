from pydantic import BaseModel
from typing import Optional, List


class QueryRequest(BaseModel):
    question:str
    top_k:Optional[int] = 3


class QueryResponse(BaseModel):
    answer:str
    sources:List[str]
