from langchain_community.vectorstores import FAISS, Chroma, Weaviate, Qdrant, Milvus, SupabaseVectorStore
from langchain.embeddings.base import Embeddings
from typing import Optional, Literal, Any
def get_vector_store(
    embeddings: Embeddings,
    documents: list,
    store_type: str = "faiss",
    **kwargs: Any
):
    """
    Create and return a vector store based on the specified type.
    Args:
        embeddings (Embeddings): An embedding object like OpenAIEmbeddings, HuggingFaceEmbeddings, etc.
        documents (List[Document]): A list of LangChain Document objects.
        store_type (str): Type of vector store. Defaults to "faiss".
        **kwargs: Additional keyword arguments required by specific vector stores.

    Returns:
        A vector store object.
    """
    store_type = store_type.lower()

    if store_type == "faiss":
        return FAISS.from_documents(documents, embeddings)

    elif store_type == "chroma":
        persist_directory = kwargs.get("persist_directory", "chroma_db")
        return Chroma.from_documents(documents, embeddings, persist_directory=persist_directory)

    elif store_type == "weaviate":
        client = kwargs.get("client")
        if client is None:
            raise ValueError("Weaviate requires a `client` argument.")
        return Weaviate.from_documents(documents, embeddings, client=client)

    elif store_type == "qdrant":
        url = kwargs.get("url", "http://localhost:6333")
        collection_name = kwargs.get("collection_name", "langchain")
        return Qdrant.from_documents(documents, embeddings, url=url, collection_name=collection_name)

    elif store_type == "milvus":
        connection_args = kwargs.get("connection_args", {})
        collection_name = kwargs.get("collection_name", "langchain")
        return Milvus.from_documents(documents, embeddings, connection_args=connection_args, collection_name=collection_name)

    elif store_type == "supabase":
        client = kwargs.get("client")
        table_name = kwargs.get("table_name", "documents")
        query_name = kwargs.get("query_name", "match_documents")
        if client is None:
            raise ValueError("SupabaseVectorStore requires a `client` argument.")
        return SupabaseVectorStore.from_documents(
            documents, embeddings, client=client,
            table_name=table_name, query_name=query_name
        )

    else:
        raise ValueError(f"Unsupported vector store type: {store_type}")
