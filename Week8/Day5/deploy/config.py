import os

# Model settings
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../Day3/quantized/gguf-model/model.gguf")

# Server settings
HOST = "localhost"
PORT = 8000

# Generation settings
MAX_TOKENS = 512
TEMPERATURE = 0.7
TOP_K = 40
TOP_P = 0.95

# Chat settings
SYSTEM_PROMPT = "You are a helpful assistant."

# Logging settings
LOG_LEVEL = "INFO"