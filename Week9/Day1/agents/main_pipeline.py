import autogen
from research_agent import research_agent
from summarizer_agent import summarizer_agent
from answer_agent import answer_agent

# User Proxy — represents the human user
user_proxy = autogen.UserProxyAgent(
    name="User",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    code_execution_config=False,
)

# Group Chat — all agents in one conversation
groupchat = autogen.GroupChat(
    agents=[user_proxy, research_agent, summarizer_agent, answer_agent],
    messages=[],
    max_round=10,
    speaker_selection_method="round_robin",
)

# Manager — orchestrates who speaks next
manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={
        "config_list": [
            {
                "model": "phi3",
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama"
            }
        ]
    }
)

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Multi-Agent Pipeline Test")
    print("Flow: User → Research → Summarize → Answer")
    print("=" * 60)

    # Start the conversation
    user_proxy.initiate_chat(
        manager,
        message="What is Agentic AI and why is it important in 2026?"
    )