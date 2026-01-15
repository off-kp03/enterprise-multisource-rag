from typing import List, Dict
import tiktoken

class TextChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        encoding_name: str = "cl100k_base",
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)

    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """
        Split raw documents into token-aware chunks.
        """
        chunks: List[Dict] = []

        for doc in documents:
            text = doc["text"]
            metadata = doc["metadata"]

            tokens = self.encoding.encode(text)
            start = 0

            while start < len(tokens):
                end = start + self.chunk_size
                chunk_tokens = tokens[start:end]

                chunk_text = self.encoding.decode(chunk_tokens)

                chunks.append(
                    {
                        "text": chunk_text,
                        "metadata": {
                            **metadata,
                            "chunk_start": start,
                            "chunk_end": end,
                        },
                    }
                )

                start += self.chunk_size - self.chunk_overlap

        return chunks
