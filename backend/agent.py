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
        from langchain.agents import AgentExecutor, create_react_agent
        from langchain_core.prompts import PromptTemplate
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
        
        # Define the ReAct prompt manually to avoid pulling from hub
        template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

        prompt = PromptTemplate.from_template(template)
        
        agent = create_react_agent(llm, tools, prompt)
        
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        return f"Error running agent: {str(e)}"

print("✓ Agent module loaded (lazy initialization)")
