from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from embeddings import process_pdf_embeddings

app = FastAPI(title="RAG Embeddings API")

class PDFRequest(BaseModel):
    pdf_path: str

@app.post("/api/ingestion/process-pdf/")
async def process_pdf(request: PDFRequest):
    try:
        chunks_count, embeddings_count = process_pdf_embeddings(request.pdf_path)
        return {
            "message": "PDF processed successfully",
            "chunks_count": chunks_count,
            "embeddings_count": embeddings_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "RAG Embeddings API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=81)