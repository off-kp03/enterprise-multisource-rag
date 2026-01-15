from fastapi import FastAPI
from app.api.routes import ingest

app = FastAPI(title="Enterprise Multi-Source RAG")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(ingest.router)
