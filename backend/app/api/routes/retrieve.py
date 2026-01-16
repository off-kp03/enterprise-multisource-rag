from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.retrieval.retriever import Retriever

router = APIRouter()
EMBEDDING_DIM = 384 
TOP_K = 5

retriever = Retriever(
    embedding_dim=EMBEDDING_DIM,
    top_k=TOP_K
)

class RetrieveRequest(BaseModel):
    query: str

@router.post("/retrieve", response_model=List[Dict])
def retrieve_docs(request: RetrieveRequest):
    try:
        results = retriever.retrieve(request.query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
