import numpy as np
from typing import List
from schemas.chunk import Chunk


class InMemoryVectorStore:
    def __init__(self):
        self.chunks: List[Chunk] = []

    def add(self, chunk: Chunk):
        self.chunks.append(chunk)

    def similarity_search(self, query_embedding: List[float], top_k: int = 10):
        if not self.chunks:
            return []

        query_vec = np.array(query_embedding)

        # Handle zero vector case
        query_norm = np.linalg.norm(query_vec)
        if query_norm == 0:
            return self.chunks[:top_k]  # Return first k chunks if query is zero

        similarities = []

        for chunk in self.chunks:
            chunk_vec = np.array(chunk.embedding)
            chunk_norm = np.linalg.norm(chunk_vec)

            # Handle zero vector case for chunk
            if chunk_norm == 0:
                score = 0
            else:
                # Calculate cosine similarity
                score = np.dot(query_vec, chunk_vec) / (query_norm * chunk_norm)

            # Handle any potential NaN values
            if np.isnan(score):
                score = 0

            similarities.append((score, chunk))

        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[0], reverse=True)

        # Return top_k chunks
        return [chunk for score, chunk in similarities[:top_k]]