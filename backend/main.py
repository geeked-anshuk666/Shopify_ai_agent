import os
import numpy as np
# Patch for Numpy 2.0 compatibility
if not hasattr(np, 'float_'):
    np.float_ = np.float64

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from agent import run_agent

load_dotenv()

# 1. Enhanced FastAPI Metadata
app = FastAPI(
    title="Shopify AI Agent API",
    description="A specialized AI agent for analyzing Shopify store data (Orders, Products, Customers) using LangChain and Gemini Pro.",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI URL (default)
    redoc_url="/redoc"     # ReDoc UI URL (cleaner alternative)
)

# CORS Setup
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
origins = [origin.strip() for origin in allowed_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Request Schema with Examples
class ChatRequest(BaseModel):
    query: str = Field(
        ..., 
        description="The natural language question to ask the AI agent.",
        examples=["How many orders were placed last week?", "Who are my top 5 customers?"]
    )

# 3. Response Schema for clearer docs
class ChatResponse(BaseModel):
    response: str = Field(
        ..., 
        description="The AI-generated answer based on Shopify data."
    )

@app.get("/", tags=["Health"])
def read_root():
    """
    Health Check endpoint to verify the service is running.
    """
    return {"status": "ok", "service": "Shopify AI Agent"}

@app.post(
    "/chat", 
    response_model=ChatResponse,
    tags=["Agent"],
    summary="Interact with the Shopify AI Agent",
    description="Sends a user query to the LangChain agent, which fetches real-time Shopify data to generate an insight."
)
def chat_endpoint(request: ChatRequest):
    query = request.query
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")
    
    try:
        # run_agent returns a string
        agent_response = run_agent(query)
        return ChatResponse(response=agent_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)