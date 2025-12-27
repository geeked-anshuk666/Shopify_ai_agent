try:
    import langchain.agents
    print("Contents of langchain.agents:")
    print(dir(langchain.agents))
    
    try:
        from langchain.agents import AgentType
        print("\nAgentType found in langchain.agents")
    except ImportError:
        print("\nAgentType NOT found in langchain.agents")

    try:
        from langchain.agents.agent_types import AgentType
        print("\nAgentType found in langchain.agents.agent_types")
    except ImportError:
        print("\nAgentType NOT found in langchain.agents.agent_types")

except ImportError as e:
    print(f"Error importing langchain.agents: {e}")
