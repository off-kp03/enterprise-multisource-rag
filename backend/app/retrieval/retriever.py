from typing import List, Dict
import numpy as np
from app.vectorstore.faiss_store import FAISSVectorStore
from app.retrieval.query_embedder import QueryEmbedder

class Retriever:
    """
    Performs vector similarity search over the FAISS index.
    Returns text, metadata, and similarity scores.
    """

    def __init__(self, embedding_dim: int, top_k: int = 5):
        self.top_k = top_k
        self.query_embedder = QueryEmbedder()
        self.vector_store = FAISSVectorStore(dim=embedding_dim)

    def retrieve(self, query: str) -> List[Dict]:
        query_vector = self.query_embedder.embed_query(query)
        query_np = np.array([query_vector]).astype("float32")
        distances, indices = self.vector_store.index.search(
            query_np, self.top_k
        )
        results = []
        for rank, idx in enumerate(indices[0]):
            if idx == -1:
                continue
            metadata = self.vector_store.metadata[idx]
            results.append(
                {
                    "rank": rank + 1,
                    "score": float(distances[0][rank]),
                    "text": metadata.get("text"),
                    "metadata": metadata,
                }
            )
        return results
