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

# Summarizer Agent
summarizer_agent = autogen.AssistantAgent(
    name="SummarizerAgent",
    system_message="""
    You are a Summarizer Agent. Your ONLY job is to summarize raw information.
    
    Rules:
    - Only work with information passed by the Research Agent
    - Create concise and clear summaries
    - Do NOT add new information
    - Do NOT give final answers
    - Keep summaries under 200 words
    - End your message with: "SUMMARY_COMPLETE - Passing to Answer Agent"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Summarizer Agent loaded successfully")
    print(f"Agent Name: {summarizer_agent.name}")