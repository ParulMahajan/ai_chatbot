from fastapi import FastAPI, Header
from router.chat import router as chat_router
from router.document import router as doc_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(doc_router)