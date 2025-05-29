import shutil
from pathlib import Path

def save_uploaded_file(file, save_dir: Path):
    """Save the uploaded file to the specified directory."""
    save_dir.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist
    file_location = save_dir / file.filename
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file_location
