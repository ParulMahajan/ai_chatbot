from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message cannot be empty")

class CollectionRequest(BaseModel):
    collection_name: str = Field(..., min_length=1, description="Collection name cannot be empty")