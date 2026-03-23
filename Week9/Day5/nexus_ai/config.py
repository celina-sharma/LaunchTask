import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Primary and Fallback models
PRIMARY_MODEL = "llama-3.3-70b-versatile"
FALLBACK_MODEL = "llama-3.1-8b-instant"

GROQ_CONFIG = {
    "api_key": GROQ_API_KEY,
    "temperature": 0.3,
    "max_tokens": 2048,
}

LOG_DIR = "logs"
LOG_FILE = "logs/nexus_ai.log"
OUTPUTS_DIR = "outputs"

MAX_RETRIES = 3

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

#task types
TASK_TYPES = {
    "CODING": "coding",
    "ARCHITECTURE": "architecture",
    "ANALYSIS": "analysis",
    "CONTENT": "content",
    "GENERAL": "general"
}

#token tracking
token_usage = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 0,
    "api_calls": 0
}

TOKEN_WARNING_LIMIT = 80000