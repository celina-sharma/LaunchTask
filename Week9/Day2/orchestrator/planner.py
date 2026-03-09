import autogen

config_list = [
    {
        "model": "phi3",
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.3,
}

# Orchestrator/Planner Agent
planner = autogen.AssistantAgent(
    name="Orchestrator",
    system_message="""
    You are an Orchestrator/Planner Agent. Your ONLY job is to break down 
    the user query into smaller tasks and assign them to Worker Agents.
    
    Rules:
    - Break every user query into exactly 3 smaller tasks
    - Clearly label them as Task 1, Task 2, Task 3
    - Each task must be specific and clear
    - Do NOT execute the tasks yourself
    - Do NOT give final answers
    - Keep your response under 100 words
    - End your message with: "TASKS_CREATED - Passing to Worker Agents"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Orchestrator Planner loaded successfully")
    print(f"Agent Name: {planner.name}")