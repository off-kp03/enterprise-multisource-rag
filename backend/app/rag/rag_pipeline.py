from typing import Dict, List
from app.retrieval.retriever import Retriever
from app.rag.prompt_builder import PromptBuilder
from app.rag.llm_client import BaseLLMClient


class RAGPipeline:
    """
    Orchestrates retrieval + prompt building + LLM generation.
    """

    def __init__(
        self,
        retriever: Retriever,
        llm_client: BaseLLMClient,
    ):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm_client = llm_client

    def run(self, question: str) -> Dict:
        retrieved_chunks: List[Dict] = self.retriever.retrieve(question)

        if not retrieved_chunks:
            return {
                "answer": "I don't know.",
                "sources": [],
            }

        prompts = self.prompt_builder.build(
            question=question,
            retrieved_chunks=retrieved_chunks,
        )
        answer_text = self.llm_client.generate(prompts)
        
        return {
            "answer": answer_text,
            "sources": retrieved_chunks,
        }
