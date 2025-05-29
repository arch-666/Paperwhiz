from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

app = FastAPI()

# Add CORS middleware BEFORE route definitions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

DATA_FOLDER = Path(__file__).parent / "data"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

def sanitize_filename(filename: str) -> str:
    safe_name = os.path.basename(filename)
    if not safe_name:
        safe_name = "uploaded_file"
    return safe_name

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filename = sanitize_filename(file.filename or "uploaded_file")
    contents = await file.read()

    save_path = DATA_FOLDER / filename
    with open(save_path, "wb") as f:
        f.write(contents)

    return {"filename": filename}
