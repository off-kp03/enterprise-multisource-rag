from pathlib import Path
from typing import List, Dict
from app.ingestion.pdf_loader import PDFLoader
from app.ingestion.chunker import TextChunker
from app.vectorstore.embeddings import EmbeddingModel
from app.vectorstore.faiss_store import FAISSVectorStore

class IngestionPipeline:
    def __init__(
        self,
        embedding_dim: int,
        vector_store_path: str = "app/data/vector_store"
    ):
        self.loader = PDFLoader()
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

        documents = self.loader.load(path)

        chunks = self.chunker.split_documents(documents)

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedder.embed(texts)

        metadatas = [
            {
                "source": chunk["source"],
                "page": chunk["page"],
                "text": chunk["text"]
            }
            for chunk in chunks
        ]

        self.vector_store.add(embeddings, metadatas)

        return {
            "status": "success",
            "documents_processed": len(documents),
            "chunks_created": len(chunks),
            "vectors_added": len(embeddings)
        }
