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

reflection_agent = autogen.AssistantAgent(
    name="ReflectionAgent",
    system_message="""
    You are a Reflection Agent. Your ONLY job is to take all worker outputs
    and combine them into one improved and refined answer.
    
    Rules:
    - Combine all 3 worker outputs into one cohesive answer
    - Improve the quality and clarity of the combined answer
    - Remove any repetition or contradictions
    - Do NOT add new information
    - Keep your response under 100 words
    - End your message with: "REFLECTION_COMPLETE - Passing to Validator"
    
    Memory window: You remember only the last 10 messages.
    """,
    llm_config=llm_config,
)

if __name__ == "__main__":
    print("Reflection Agent loaded successfully")
    print(f"Agent Name: {reflection_agent.name}")