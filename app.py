from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from data_processing import process_uploaded_file

app = FastAPI()

# Store the files locally for now
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    """
    Endpoint to upload a file for processing
    """

    # Validate the file type
    if file.content_type not in ["text/csv", "application/json"]:
        raise HTTPException(status_code=400, detail="Only CSV and JSON file types are allowed")
    
    # Save the file 
    file_path = UPLOAD_DIR / file.filename 
    with file_path.open("wb") as f:
        f.write(await file.read())

    return {"filename": file.filename, 
            "message": "File uploaded successfully"}

@app.get("/files/")
async def list_files():

    """
    Endpoint to get all uploaded files
    """

    # List uploaded files
    files = [file.name for file in UPLOAD_DIR.iterdir()]
    return{"files": files}

@app.post("/process/")
async def process_file(file_name: str):
    
    """
    Endpoint to process an uploaded file and extract insights
    """

    file_path = UPLOAD_DIR / file_name 
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return process_uploaded_file(file_path)