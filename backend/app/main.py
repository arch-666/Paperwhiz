from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from transformers.pipelines import pipeline
from utils.file_utils import sanitize_filename
from utils.file_utils import extract_text_from_file
from utils.doc_loaders import load_document
from utils.text_splitters import smart_splitter
from tools.rag_tool import rag_tool
from langchain_community.embeddings import HuggingFaceEmbeddings



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
    text = text[:2000]
    if not text:
        return {"error": "No text extracted from the file."}
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    result = rag_tool(save_path, filename,embeddings=embedding_model)['retriever']
    if "error" in result:
        return result
    query = text[:100]
    retrieved = result.invoke(query)
    print(retrieved)
    return {"filename": filename, "summary": summary}
