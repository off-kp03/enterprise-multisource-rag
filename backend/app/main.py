from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import ingest
from app.api.routes import retrieve
from app.api.routes import rag
from app.api.routes import auth

app = FastAPI(title="Enterprise Multi-Source RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(ingest.router)
app.include_router(retrieve.router)
app.include_router(rag.router)
app.include_router(auth.router)
