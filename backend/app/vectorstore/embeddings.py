from typing import List
import torch
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name, device=self.device)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Convert a list of texts into embedding vectors.
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )
        return embeddings.tolist()
