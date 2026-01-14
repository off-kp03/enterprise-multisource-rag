from fastapi import FastAPI

app = FastAPI(title="Enterprise Multi-Source RAG")

@app.get("/health")
def health_check():
    return {"status": "ok"}
