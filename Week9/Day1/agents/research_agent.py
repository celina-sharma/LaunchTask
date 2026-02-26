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

# Research Agent
research_agent = autogen.AssistantAgent(
    name="ResearchAgent",
    system_message="""
    You are a Research Agent. Your ONLY job is to find and present raw information.
    
    Rules:
    - Only gather and present facts and raw information
    - Do NOT summarize anything
    - Do NOT provide final answers
    - Present information in bullet points
    - End your message with: "RESEARCH_COMPLETE - Passing to Summarizer"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Research Agent loaded successfully")
    print(f"Agent Name: {research_agent.name}")