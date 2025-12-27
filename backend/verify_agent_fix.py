import sys
import os

# Add backend directory to sys.path so we can import 'agent' and 'tools'
current_dir = os.getcwd()
backend_dir = os.path.join(current_dir, "backend")
sys.path.append(backend_dir)

print(f"Added to path: {backend_dir}")

# Mock GOOGLE_API_KEY
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "mock_key"

try:
    import agent
    print("Agent module imported successfully.")
    
    from langchain.agents import create_react_agent
    print("create_react_agent imported successfully.")
    
except Exception as e:
    print(f"FAILED to load agent: {e}")
    import traceback
    traceback.print_exc()
