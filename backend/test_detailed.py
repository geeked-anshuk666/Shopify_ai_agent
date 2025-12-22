print("Step 1: Basic imports...")
import os
import pandas as pd
import datetime
import math
from dotenv import load_dotenv
print("✓ Basic imports OK")

print("Step 2: Loading env...")
load_dotenv()
print("✓ Env loaded")

print("Step 3: LangChain agents...")
from langchain.agents import AgentType, initialize_agent
print("✓ LangChain agents OK")

print("Step 4: Google GenAI...")
from langchain_google_genai import ChatGoogleGenerativeAI
print("✓ Google GenAI OK")

print("Step 5: Python REPL Tool...")
from langchain_experimental.tools.python.tool import PythonAstREPLTool
print("✓ REPL Tool OK")

print("Step 6: Shopify tools...")
from tools import get_shopify_data
print("✓ Shopify tools OK")

print("Step 7: Initializing LLM...")
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Warning: GOOGLE_API_KEY not found")
    api_key = "dummy"  # Just for testing

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key,
    temperature=0
)
print("✓ LLM initialized")

print("Step 8: Creating tools...")
python_repl = PythonAstREPLTool(
    locals={"pd": pd, "datetime": datetime, "math": math}
)
tools = [get_shopify_data, python_repl]
print("✓ Tools created")

print("Step 9: Creating agent...")
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)
print("✓ Agent created successfully!")
