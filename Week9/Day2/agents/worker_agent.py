import autogen

# Connecting to Phi-3 running locally via Ollama
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

# Worker Agent 1
worker1 = autogen.AssistantAgent(
    name="Worker1",
    system_message="""
    You are Worker Agent 1. You will receive Task 1 from the Orchestrator.
    
    Rules:
    - Only execute Task 1 assigned to you
    - Do NOT work on other tasks
    - Give a detailed response for your task
    - End your message with: "TASK1_COMPLETE"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

# Worker Agent 2
worker2 = autogen.AssistantAgent(
    name="Worker2",
    system_message="""
    You are Worker Agent 2. You will receive Task 2 from the Orchestrator.
    
    Rules:
    - Only execute Task 2 assigned to you
    - Do NOT work on other tasks
    - Give a detailed response for your task
    - Keep your response under 100 words
    - End your message with: "TASK2_COMPLETE"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

# Worker Agent 3
worker3 = autogen.AssistantAgent(
    name="Worker3",
    system_message="""
    You are Worker Agent 3. You will receive Task 3 from the Orchestrator.
    
    Rules:
    - Only execute Task 3 assigned to you
    - Do NOT work on other tasks
    - Give a detailed response for your task
    - End your message with: "TASK3_COMPLETE"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Worker Agents loaded successfully")
    print(f"Worker 1: {worker1.name}")
    print(f"Worker 2: {worker2.name}")
    print(f"Worker 3: {worker3.name}")