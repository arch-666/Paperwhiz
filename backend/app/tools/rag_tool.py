from utils.doc_loaders import load_document
from utils.text_splitters import smart_splitter
from typing import Union
from pathlib import Path
from utils.vector_store import get_vector_store
def rag_tool(path: Union[str,Path] ,filename: str, embeddings) -> dict:
    doc  =  load_document(path, filename.split('.')[-1].lower())
    if not doc:
        return {"error": "Document loading failed."}
    chunks = smart_splitter(doc)
    if not chunks:
        return {"error": "Document splitting failed."}
    vector_store = get_vector_store(embeddings, chunks)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    if not vector_store or not retriever:
        return {"error": "Vector store or retriever creation failed."}
    return {
        "filename": filename,
        "chunks": [chunk.page_content for chunk in chunks],
        "vector_store": vector_store,
        "retriever": retriever
    }
    # return {"filename": filename, "chunks": [chunk.page_content for chunk in chunks], "vector_store": vector_store, "retriever": retriever}