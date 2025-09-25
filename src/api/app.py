
from fastapi import FastAPI
from pydantic import BaseModel
from .rag import answer

app = FastAPI()

class Query(BaseModel):
    question: str

@app.get("/healthz")
def health():
    return {"ok": True}

@app.post("/api/chat")
def chat_api(q: Query):
    return {"answer": answer(q.question)}
