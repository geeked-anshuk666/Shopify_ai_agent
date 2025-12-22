import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

app = FastAPI(title="Shopify AI Agent")

# CORS
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Shopify AI Agent"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    try:
        response = run_agent(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
