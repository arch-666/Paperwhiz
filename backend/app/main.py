from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

app = FastAPI()

# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ideally restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the directory where files will be saved (outside the folder where main.py is)
DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"  # One level up from the current folder
DATA_FOLDER.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Validate file size (optional, e.g., 10MB max)
    max_size = 10 * 1024 * 1024  # 10MB limit
    if len(await file.read()) > max_size:
        return {"error": "File is too large. Please upload a file smaller than 10MB."}
    
    # Move the cursor back to the beginning after reading
    await file.seek(0)

    # Save the file to the data folder
    file_location = DATA_FOLDER / file.filename
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)  # Efficiently copy the file content
        return {"filename": file.filename, "location": str(file_location), "size": len(contents)}
    except Exception as e:
        return {"error": f"Failed to save file: {e}"}
