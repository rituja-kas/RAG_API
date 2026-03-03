from pydantic import BaseModel
from typing import List

class Chunk(BaseModel):
    id: int
    text: str
    embedding:List[float]
