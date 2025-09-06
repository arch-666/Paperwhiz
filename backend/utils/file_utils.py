import os
import  pdfplumber
import docx
from pathlib import Path
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
