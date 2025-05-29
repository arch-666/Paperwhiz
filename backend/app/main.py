from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from transformers.pipelines import pipeline
import os
import pdfplumber
import docx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FOLDER = Path(__file__).parent / "data"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

# Initialize summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def sanitize_filename(filename: str) -> str:
    safe_name = os.path.basename(filename)
    if not safe_name:
        safe_name = "uploaded_file"
    return safe_name

def extract_text_from_file(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    if ext == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")
    elif ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif ext == ".docx":
        doc = docx.Document(str(file_path))
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return ""

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    filename = sanitize_filename(file.filename or "uploaded_file")
    contents = await file.read()

    save_path = DATA_FOLDER / filename
    with open(save_path, "wb") as f:
        f.write(contents)

    # Extract text and summarize
    text = extract_text_from_file(save_path)
    if not text.strip():
        return {"error": "Could not extract text from file."}
    
    # Summarize (limit to first 1000 tokens to fit model limits)
    text = text[:2000]  # simple truncation to avoid token limit errors
    result = summarizer(text, max_length=130, min_length=30, do_sample=False)
    if result is None:
        return {"error": "Summarization failed."}
    if isinstance(result, list):
        result_list = result
    else:
        try:
            result_list = list(result)
        except TypeError:
            return {"error": "Summarization failed."}
    if not result_list or not isinstance(result_list[0], dict) or "summary_text" not in result_list[0]:
        return {"error": "Summarization failed."}
    summary = result_list[0]["summary_text"]
    
    return {"filename": filename, "summary": summary}
