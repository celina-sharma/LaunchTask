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

# Validator Agent
validator = autogen.AssistantAgent(
    name="ValidatorAgent",
    system_message="""
    You are a Validator Agent. Your ONLY job is to check the final answer 
    for errors and approve or reject it.
    
    Rules:
    - Check the answer from Reflection Agent for any errors
    - Check for factual errors, contradictions or incomplete answers
    - If answer is good: End with "VALIDATED - Final Answer Approved"
    - If answer has errors: End with "REJECTED - [reason for rejection]"
    - Do NOT add new information
    - Do NOT rewrite the answer
    - Keep your response under 100 words
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Validator Agent loaded successfully")
    print(f"Agent Name: {validator.name}")