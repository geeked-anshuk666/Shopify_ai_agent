try:
    import langchain.agents
    print(f"Has initialize_agent: {'initialize_agent' in dir(langchain.agents)}")
    print(f"Has create_react_agent: {'create_react_agent' in dir(langchain.agents)}")
    
    from langchain.agents import AgentType
    print("AgentType found")
except ImportError:
    print("AgentType NOT found")
except Exception as e:
    print(f"Error: {e}")
