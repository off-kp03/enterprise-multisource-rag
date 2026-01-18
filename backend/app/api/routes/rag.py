from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.deps import get_db
from app.db.models.chat import Chat
from app.db.models.message import Message

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
def run_rag(
    request: RAGRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        chat = Chat(
            user_id=current_user.id,
            title=request.question[:50]
        )
        db.add(chat)
        db.flush()  

        rag_result = rag_pipeline.run(request.question)
        answer_text = rag_result["answer"]

        user_msg = Message(
            chat_id=chat.id,
            role="user",
            content=request.question
        )

        assistant_msg = Message(
            chat_id=chat.id,
            role="assistant",
            content=answer_text
        )

        db.add_all([user_msg, assistant_msg])
        db.commit()

        return {
            "answer": answer_text,
            "sources": rag_result.get("sources", []),
            "chat_id": chat.id
        }


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
