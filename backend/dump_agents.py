import langchain.agents
with open("backend/langchain_agents_dir.txt", "w") as f:
    f.write(str(dir(langchain.agents)))
