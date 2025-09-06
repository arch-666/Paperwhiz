from typing import List, Union
from langchain_core.documents import Document
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
    HTMLHeaderTextSplitter,
    Language,
)

def smart_splitter(documents: Union[str, List[Document]], doc_type: str = "auto") -> List[Document]:
    """
    Smart splitter for various doc types using latest LangChain splitters
    """
    # Normalize input
    if isinstance(documents, str):
        documents = [Document(page_content=documents)]
    
    content_sample = documents[0].page_content.lower()
    
    # Auto-detect type
    if doc_type == "auto":
        if "<html" in content_sample:
            doc_type = "html"
        elif "# " in content_sample or "```" in content_sample:
            doc_type = "markdown"
        elif any(kw in content_sample for kw in ["def ", "class ", "function "]):
            doc_type = "code"
        else:
            doc_type = "recursive"
    
    # Handle splitters
    if doc_type == "html":
        splitter = HTMLHeaderTextSplitter(headers_to_split_on=[
            ("h1", "Header 1"),
            ("h2", "Header 2"),
            ("h3", "Header 3"),
        ])
        return splitter.split_text(documents[0].page_content)
    
    elif doc_type == "markdown":
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ])
        return splitter.split_text(documents[0].page_content)
    
    elif doc_type == "code":
        splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=500,
            chunk_overlap=50
        )
        return splitter.split_documents(documents)
    
    elif doc_type == "token":
        splitter = TokenTextSplitter(chunk_size=256, chunk_overlap=32)
    
    elif doc_type == "char":
        splitter = CharacterTextSplitter(separator="\n\n", chunk_size=1000, chunk_overlap=100)
    
    else:  # default recursive
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    
    return splitter.split_documents(documents)
