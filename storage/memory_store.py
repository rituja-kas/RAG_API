import numpy as np
from typing import List
from schemas.chunk import Chunk

class InMemoryVectorStore:
    def __init__(self):
        self.chunks: List[Chunk] = []

    def add(self, chunk: Chunk):
        self.chunks.append(chunk)

    def similarity_search(self,query_embedding:List[float],top_k:int=10):
        if not self.chunks:
            return []

        query_vec = np.array(query_embedding)
        similarities = []

        for chunk in self.chunks:
            chunk_vec = np.array(chunk.embedding)
            score = np.dot(query_vec,chunk_vec)/(np.linalg.norm(query_vec) * np.linalg.norm(chunk_vec))
            similarities.append((score,chunk))

            return [chunk for _,chunk in similarities[:top_k]]




