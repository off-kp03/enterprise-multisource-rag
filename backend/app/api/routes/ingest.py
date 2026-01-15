import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from ingestion.pipeline import IngestionPipeline

router = APIRouter()

UPLOAD_DIR = Path("backend/app/data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# IMPORTANT:
EMBEDDING_DIM = 384

pipeline = IngestionPipeline(embedding_dim=EMBEDDING_DIM)

@router.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_path = UPLOAD_DIR / file.filename

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = pipeline.ingest_pdf(str(file_path))
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        file.file.close()
