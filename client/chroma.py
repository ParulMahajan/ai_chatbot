import chromadb
from langchain_chroma import Chroma
import os
from langchain_huggingface import HuggingFaceEmbeddings
from functools import lru_cache

chroma_host = os.getenv("CHROMA_HOST")

def get_chroma_client():
    """Initialize and return a ChromaDB client."""
    if not chroma_host:
        raise ValueError("CHROMA_HOST environment variable is not set.")

    return chromadb.HttpClient(host=chroma_host, port=8000)

@lru_cache(maxsize=4)  # Cache up to 4 different collections
def get_vector_store(collection: str ="maxbit"):

    if not collection:
        raise ValueError("Collection name must be provided.")

    # Initialize the embedding function
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vector_store = Chroma(
        client=get_chroma_client(),
        collection_name=collection,
        embedding_function=embedding_function,
    )
    return vector_store

