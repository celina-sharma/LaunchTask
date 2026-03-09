import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# LLM Config for AutoGen
LLM_CONFIG = {
    "config_list": [
        {
            "model": "llama-3.3-70b-versatile",
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": GROQ_API_KEY
        }
    ],
    "temperature": 0.3,
    "timeout": 60,
}

# Logging
LOG_DIR = "logs"
LOG_FILE = "logs/nexus_ai.log"

# Memory
MAX_MESSAGES = 10

# Agent names
AGENTS = [
    "Orchestrator",
    "Planner",
    "Researcher",
    "Coder",
    "Analyst",
    "Critic",
    "Optimizer",
    "Validator",
    "Reporter"
]

# Max retries for failure recovery
MAX_RETRIES = 3

