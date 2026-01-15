from pathlib import Path
from typing import Dict

from app.ingestion.pdf_loader import load_pdf
from app.ingestion.chunker import TextChunker
from app.vectorstore.embeddings import EmbeddingModel
from app.vectorstore.faiss_store import FAISSVectorStore


class IngestionPipeline:
    def __init__(
        self,
        embedding_dim: int,
        vector_store_path: str = "app/data/vector_store"
    ):
        self.chunker = TextChunker()
        self.embedder = EmbeddingModel()
        self.vector_store = FAISSVectorStore(
            dim=embedding_dim,
            store_path=vector_store_path
        )

    def ingest_pdf(self, file_path: str) -> Dict:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        documents = load_pdf(str(path))

        chunks = self.chunker.chunk_documents(documents)

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedder.embed_texts(texts)

        metadatas = [chunk["metadata"] for chunk in chunks]
        self.vector_store.add(embeddings, metadatas)

        return {
            "status": "success",
            "documents_processed": len(documents),
            "chunks_created": len(chunks),
            "vectors_added": len(embeddings),
        }
