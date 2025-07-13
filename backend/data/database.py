import json
from fastapi import FastAPI, HTTPException
from .data_ingestion import DatabaseConfig
from pydantic import BaseModel

class DocLink(BaseModel):
    doc_link: str

app = FastAPI(
    title="NIA AI Database API",
    description="API for ingesting patient data in the NIA AI Database."
)
db_config = DatabaseConfig()

@app.get("/")
def read_root():
    return {"message": "Post Discharge Medical AI Database API is running."}

@app.post("/api/database/add_patients/", tags=["Adding Patients"])
async def add_patients(patients: DocLink):
    try:
        document_link = patients.doc_link
        with open(document_link, "r") as file:
            patients = json.load(file)
        result = db_config.database_connection(patients)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=81)