import os
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
import docx
import pdfplumber
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    pipeline,
    GenerationConfig,
)

# --- 1. CONFIGURATION ---
DATA_FOLDER = Path(__file__).parent / "data"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)
MODEL_NAME = "distilgpt2"

ml_models = {}


def load_summarizer():
    print(f"Loading model: {MODEL_NAME}...")

    # By passing MODEL_NAME as a string, the pipeline
    # handles the task-to-model mapping automatically.
    summarizer_pipe = pipeline(
        "text-generation", model=MODEL_NAME, device=-1  # -1 for CPU, 0 for GPU
    )

    return {
        "pipeline": summarizer_pipe,
        "tokenizer": summarizer_pipe.tokenizer,
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Offload loading to a thread so startup doesn't hang the loop
    loop = asyncio.get_running_loop()
    try:
        ml_models["res"] = await loop.run_in_executor(None, load_summarizer)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Startup Error: {e}")
    yield
    ml_models.clear()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 2. HELPERS ---
def extract_text(file_path: Path) -> str:
    """Theory: Heavy I/O should be wrapped in a thread when called from async."""
    ext = file_path.suffix.lower()
    try:
        if ext == ".txt":
            return file_path.read_text(encoding="utf-8", errors="ignore")
        elif ext == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                return " ".join([page.extract_text() or "" for page in pdf.pages])
        elif ext == ".docx":
            doc = docx.Document(str(file_path))
            return " ".join([p.text for p in doc.paragraphs])
    except Exception as e:
        print(f"Extraction error: {e}")
    return ""


# --- 3. ENDPOINTS ---
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    loop = asyncio.get_running_loop()

    # 1. Check if model is ready
    res = ml_models.get("res")
    if not res:
        raise HTTPException(
            status_code=503,
            detail="Model is still loading. Please try again in a few seconds.",
        )

    # 2. Save file (Async I/O)
    filename = os.path.basename(file.filename or "file")
    save_path = DATA_FOLDER / filename
    content = await file.read()

    # Writing to disk is blocking; for true scale, use a thread
    await loop.run_in_executor(None, lambda: save_path.write_bytes(content))

    # 3. Extract text (Offloaded to thread)
    text = await loop.run_in_executor(None, extract_text, save_path)

    if not text.strip():
        raise HTTPException(status_code=400, detail="File is empty or unreadable.")

    summarizer = res["pipeline"]
    tokenizer = res["tokenizer"]

    try:
        # 4. Tokenization (Fast, usually okay on main thread)
        tokens = tokenizer.encode(
            text, truncation=True, max_length=1024, return_tensors="pt"
        )
        truncated_text = tokenizer.decode(tokens[0], skip_special_tokens=True)

        gen_config = GenerationConfig(
            max_new_tokens=150,
            min_length=40,
            do_sample=False,
            bos_token_id=tokenizer.bos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.pad_token_id,
        )

        # 2. Pass the config to the pipeline
        result = await loop.run_in_executor(
            None, lambda: summarizer(truncated_text, generation_config=gen_config)
        )

        return {"filename": filename, "summary": result[0]["summary_text"]}
    except Exception as e:
        return {"error": f"Summarization failed: {str(e)}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
