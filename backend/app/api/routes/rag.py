from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.retrieval.retriever import Retriever
from app.rag.llm_client import MockLLMClient
# from app.rag.llm_client import OpenAILikeClient
from app.rag.rag_pipeline import RAGPipeline

router = APIRouter()

EMBEDDING_DIM = 384

retriever = Retriever(embedding_dim=EMBEDDING_DIM)
llm_client = MockLLMClient()
# llm_client = OpenAILikeClient(
#     model_name="gpt-4o-mini"
# )

rag_pipeline = RAGPipeline(
    retriever=retriever,
    llm_client=llm_client,
)


class RAGRequest(BaseModel):
    question: str


@router.post("/rag")
def run_rag(request: RAGRequest):
    try:
        return rag_pipeline.run(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
