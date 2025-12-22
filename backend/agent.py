import os
import pandas as pd
import datetime
import math
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from tools import get_shopify_data

# Initialize Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Warning: GOOGLE_API_KEY not found in environment.")

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key,
    temperature=0
)

# Setup Tools
python_repl = PythonAstREPLTool(
    locals={"pd": pd, "datetime": datetime, "math": math},
    description="A Python REPL. Use this to execute python code for data analysis, filtering, date calculations, and creating tables. Input should be a valid python script. When you have the data, always use this tool to process it and generate tables or aggregations."
)

tools = [get_shopify_data, python_repl]

# Prompt
template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

**Role**: You are an expert Shopify Data Analyst. Your goal is to help store owners understand their business data.

**Instructions**:
1. ALWAYS use `get_shopify_data` to fetch data first. Do NOT Hallucinate data.
2. If the user asks for orders in a specific timeframe (e.g., "last 7 days"), fetch the data (you may need to fetch more recent orders) and then use `python_repl` with `datetime` to filter them accurately.
3. For "How many..." or "Sum of..." questions, fetch data then use Python to calculate.
4. When asked for a table, generate a Markdown table.
5. If the user asks for a chart, you can't render it directly, but you can say "I have analyzed the data..." and provide the data points in a table format.
6. **NEVER** output raw python code to the user. Execute it in the REPL and only show the *result* or *interpretation*.
7. If you cannot find data, say so.
8. Be professional and concise.

**Format**:
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

agent = create_react_agent(llm, tools, prompt=PromptTemplate.from_template(template))

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    max_iterations=10
)

def run_agent(query: str):
    try:
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        return f"Error running agent: {str(e)}"
