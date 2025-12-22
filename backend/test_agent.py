import traceback
import sys

try:
    print("Importing agent...")
    from agent import run_agent
    print("✓ Agent imported successfully!")
    print("Testing agent...")
    result = run_agent("test query")
    print(f"✓ Agent test result: {result[:100]}...")
except Exception as e:
    print(f"✗ Error: {e}")
    traceback.print_exc()
    sys.exit(1)
