from fastapi import APIRouter,UploadFile, File, Form
from request.Enum import DocumentType
from request.req import CollectionRequest
from service.doc_service import get_all_collections, desc_collection, upload_document, delete_collection, \
    delete_document

router = APIRouter()

@router.get("/collection")
async def get_collection() :
    return get_all_collections();

@router.get("/desc-collection")
async def get_collection() :
    return desc_collection();

@router.post("/delete-collection")
async def del_collection(request: CollectionRequest):
    return delete_collection(request.collection_name);

@router.post("/delete-document/{document_id}")
async def del_document(document_id: str):
    return delete_document(document_id);

@router.post("/add-document")
async def upload(
        files: list[UploadFile] = File(...),
        doc_type: DocumentType = Form(...),
        ) -> dict:

    result = await upload_document(files, doc_type)
    return result