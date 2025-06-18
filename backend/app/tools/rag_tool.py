from utils.doc_loaders import load_document
from utils.text_splitters import smart_splitter
from typing import Union
from pathlib import Path    
def rag_tool(path: Union[str,Path] ,filename: str) :
    doc  =  load_document(path, filename.split('.')[-1].lower())
    print(doc[0])
    if not doc:
        return {"error": "Document loading failed."}
    chunks = smart_splitter(doc)
    if not chunks:
        return {"error": "Document splitting failed."}
    print(f"Document split into {len(chunks)} chunks.")
    return {"filename": filename, "chunks": [chunk.page_content for chunk in chunks]}