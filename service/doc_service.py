from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredRTFLoader
from langchain_core.documents import Document
import os
from model.chain import  chain_with_history
from client.chroma import get_chroma_client, get_vector_store
from request.Enum import DocumentType, ALLOWED_EXTENSIONS
from util_ai.logger import logger as log

async def chat_response(message: str, user_id: str) -> str:

    log.info(f"User message: {message}")
    log.info(f"User user_id: {user_id}")
    my_config = {"configurable": {"session_id": user_id}}

    try:
        response = await chain_with_history.ainvoke( input={"input": message},
                                          config=my_config)
        #log.info(response)
        log.info(f"llm response =: {response['output']}")
        return response["output"]
    except Exception as e:
        log.error(f"Error in chat_response: {str(e)}")
        raise

async def upload_document(files: list[UploadFile], doc_type: DocumentType) -> dict:

    # Create temp directory if it doesn't exist
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)

    vector_store = get_vector_store()
    success_files = []
    failed_files = []

    for file in files:
        filename = file.filename

        # Validate filename has an extension
        _, file_ext = os.path.splitext(filename)
        log.info(f"file ext: {file_ext}")
        file_ext = file_ext.lower().lstrip('.')

        # Validate extensions
        allowed = ALLOWED_EXTENSIONS.get(doc_type, set())
        if file_ext not in allowed:
            error_msg = f"Invalid file extension: .{file_ext} for {doc_type.name}. Allowed: {', .'.join(allowed)}"
            log.warning(error_msg)
            failed_files.append({"filename": filename, "error": error_msg})
            continue

        temp_path = os.path.join(temp_dir, file.filename)

        try:
            # Save file content to temp file
            content = await file.read()
            with open(temp_path, "wb") as f:
                f.write(content)

            # Get documents using the appropriate loader
            documents = get_documents(temp_path, doc_type)

            # Add processed documents to vector store
            vector_store.add_documents(documents=documents)
            success_files.append(filename)

        except Exception as e:
            log.error(f"Error processing {filename}: {str(e)}")
            failed_files.append({"filename": filename, "error": str(e)})
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    return {
        "status": "partial_success" if failed_files else "success",
        "processed": success_files,
        "failed": failed_files
    }

def get_documents(file_path: str, doc_type: DocumentType) -> list[Document]:
    if doc_type == DocumentType.PDF:
        log.info(f"File type: {doc_type.name}")
        loader = PyPDFLoader(file_path)
        return loader.load()
    elif doc_type == DocumentType.TXT:
        loader = TextLoader(file_path)
        return loader.load()
    elif doc_type == DocumentType.RTF:
        loader = UnstructuredRTFLoader(file_path)
        return loader.load()

    raise ValueError(f"Unsupported document type: {doc_type}")


def get_all_collections():
    """Retrieve and return all collections from the ChromaDB client."""
    client = get_chroma_client()
    collections = client.list_collections()
    return collections

def delete_collection(collection_name: str) -> dict:
    if not collection_name or collection_name.strip() == "" :
        raise ValueError("Collection name must be provided.")

    client = get_chroma_client()
    log.info(f"Attempting to delete collection: {collection_name}")

    try:
        client.delete_collection(name=collection_name)
        log.info(f"Successfully deleted collection: {collection_name}")
        return {
            "status": "success",
        }
    except Exception as e:
        log.error(f"Error deleting collection {collection_name}: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to delete collection: {str(e)}"
        }

def delete_document(document_id: int) ->dict:
    if not document_id:
        raise ValueError("Document ID must be provided.")

    vector_store = get_vector_store()
    log.info(f"Attempting to delete document with ID: {document_id}")

    try:
        vector_store.delete(ids=[document_id])
        log.info(f"Successfully deleted document with ID: {document_id}")
        return {
            "status": "success",
        }
    except Exception as e:
        log.error(f"Error deleting document with ID {document_id}: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to delete document: {str(e)}"
        }

def desc_collection() -> dict:

    result = {
        "collections": []
    }
    collections = get_all_collections()
    if not collections:
        return result

    for col in collections:
        vector_store = get_vector_store(col.name)
        resp = vector_store.get()

        collection_info = {
            "name": col.name,
            "document_count": len(resp['documents']),
            "documents": []
        }

        for i in range(len(resp["documents"])):
            document_info = {
                "id": resp['ids'][i],
                "content": resp['documents'][i],
                "metadata": resp['metadatas'][i]
            }
            collection_info["documents"].append(document_info)

        result["collections"].append(collection_info)

    return result


