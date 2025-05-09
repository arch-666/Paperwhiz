from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

app = FastAPI()

# Allow frontend to access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ideally restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the directory where files will be saved (same folder as main.py)
DATA_FOLDER = Path(__file__).resolve().parent / "data"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Save the file to the data folder
    file_location = DATA_FOLDER / file.filename
    with open(file_location, "wb") as f:
        f.write(contents)
    return {"filename": file.filename, "location": str(file_location)}
