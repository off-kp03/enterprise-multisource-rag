from pathlib import Path
from typing import List, Dict
import json
import faiss
import numpy as np


class FAISSVectorStore:
    def __init__(self, dim: int, store_path: str = "app/data/vector_store"):
        self.dim = dim
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)

        self.index_file = self.store_path / "index.faiss"
        self.meta_file = self.store_path / "metadata.json"

        self.index = faiss.IndexFlatL2(self.dim)
        self.metadata: List[Dict] = []

        if self.index_file.exists() and self.meta_file.exists():
            self._load()

    def add(self, vectors: List[List[float]], metadatas: List[Dict]):
        vectors_np = np.array(vectors).astype("float32")

        if vectors_np.shape[1] != self.dim:
            raise ValueError("Embedding dimension mismatch")

        self.index.add(vectors_np)
        self.metadata.extend(metadatas)

        self._save()

    def search(self, query_vector: List[float], top_k: int = 5):
        query_np = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_np, top_k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])

        return results

    def _save(self):
        faiss.write_index(self.index, str(self.index_file))
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2)

    def _load(self):
        self.index = faiss.read_index(str(self.index_file))
        with open(self.meta_file, "r", encoding="utf-8") as f:
            self.metadata = json.load(f)
