import os
from dotenv import load_dotenv

load_dotenv()

# Delayed imports to avoid numpy issues at module level
def run_agent(query: str):
    """Run the agent with the given query"""
    try:
        # Import inside function to delay numpy loading
        import pandas as pd
        import datetime
        import math
        from langchain.agents import AgentType, initialize_agent
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_experimental.tools.python.tool import PythonAstREPLTool
        from tools import get_shopify_data
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "Error: GOOGLE_API_KEY not found in environment. Please set it in your .env file."
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0
        )
        
        python_repl = PythonAstREPLTool(
            locals={"pd": pd, "datetime": datetime, "math": math},
            description="A Python REPL. Use this to execute python code for data analysis, filtering, date calculations, and creating tables."
        )
        
        tools = [get_shopify_data, python_repl]
        
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        result = agent.run(query)
        return result
    except Exception as e:
        return f"Error running agent: {str(e)}"

print("✓ Agent module loaded (lazy initialization)")
