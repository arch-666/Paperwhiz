from typing import Union
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredEmailLoader,
    UnstructuredHTMLLoader,
    UnstructuredCSVLoader,
    UnstructuredXMLLoader,
    UnstructuredFileLoader
)

def load_document(file_path: Union[str, Path], file_type: str):
    """
    Load a document based on its type.

    Args:
        file_path (str): Path to the document file.
        file_type (str): Type of the document (e.g., 'txt', 'pdf', 'docx').

    Returns:
        List[Document]: Loaded document(s).
    """
    file_path_str = str(file_path)
    file_type = file_type.lower()

    if file_type == "txt":
        return TextLoader(file_path).load()
    elif file_type == "pdf":
        return PyPDFLoader(file_path).load()
    elif file_type == "docx":
        return Docx2txtLoader(file_path).load()
    elif file_type == "markdown":
        return UnstructuredMarkdownLoader(file_path).load()
    elif file_type == "pptx":
        return UnstructuredPowerPointLoader(file_path).load()
    elif file_type == "xlsx":
        return UnstructuredExcelLoader(file_path).load()
    elif file_type == "email":
        return UnstructuredEmailLoader(file_path).load()
    elif file_type == "html":
        return UnstructuredHTMLLoader(file_path).load()
    elif file_type == "csv":
        return UnstructuredCSVLoader(file_path_str).load()
    elif file_type == "xml":
        return UnstructuredXMLLoader(file_path).load()
    else:
        # Fallback: attempt with generic UnstructuredFileLoader
        return UnstructuredFileLoader(file_path).load()
