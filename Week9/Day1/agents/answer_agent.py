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
    "temperature": 0.5,
}

# Answer Agent
answer_agent = autogen.AssistantAgent(
    name="AnswerAgent",
    system_message="""
    You are an Answer Agent. Your ONLY job is to give the final answer to the user.
    
    Rules:
    - Only work with summaries passed by the Summarizer Agent
    - Write in a friendly and clear tone
    - Give a direct and complete final answer
    - Do NOT do new research
    - Do NOT re-summarize
    - End your message with: "ANSWER_DELIVERED"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Answer Agent loaded successfully")
    print(f"Agent Name: {answer_agent.name}")