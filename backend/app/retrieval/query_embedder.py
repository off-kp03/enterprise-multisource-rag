from typing import List
from app.vectorstore.embeddings import EmbeddingModel

class QueryEmbedder:
    """
    Converts a user query into an embedding vector.
    Uses the same embedding model as document ingestion.
    """

    def __init__(self):
        self.embedder = EmbeddingModel()

    def embed_query(self, query: str) -> List[float]:
        if not query or not query.strip():
            raise ValueError("Query text cannot be empty")

        vector = self.embedder.embed_texts([query])[0]
        return vector
