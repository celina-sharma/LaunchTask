import uuid
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
import re
from deploy.model_loader import get_model
from deploy.config import TEMPERATURE, TOP_K, TOP_P, MAX_TOKENS, SYSTEM_PROMPT, HOST, PORT

# Setup logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Local LLM API",
    description="Local LLM API using TinyLlama GGUF model",
    version="1.0.0"
)

# Request Models
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = MAX_TOKENS
    temperature: Optional[float] = TEMPERATURE
    top_k: Optional[int] = TOP_K
    top_p: Optional[float] = TOP_P

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    system_prompt: Optional[str] = SYSTEM_PROMPT
    max_tokens: Optional[int] = MAX_TOKENS
    temperature: Optional[float] = TEMPERATURE
    top_k: Optional[int] = TOP_K
    top_p: Optional[float] = TOP_P


# Routes
@app.get("/")
def root():
    return {"message": "Local LLM API is running!"}

@app.post("/generate")
def generate(request: GenerateRequest):
    request_id = str(uuid.uuid4())
    logger.info(f"Request ID: {request_id} - /generate called")
    
    if not is_coding_related(request.prompt):
        logger.warning(f"Request ID: {request_id} - Rejected non-coding prompt")
        return {
            "request_id": request_id,
            "prompt": request.prompt,
            "response": "I'm sorry! I can only answer coding and AI/ML related questions."
        }

    model = get_model()

    formatted_prompt = f"""### Instruction:
{request.prompt}

### Response:
"""

    output = model(
        formatted_prompt,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p,
        echo=False
    )

    response = output['choices'][0]['text']

    logger.info(f"Request ID: {request_id} - Response generated")

    return {
        "request_id": request_id,
        "prompt": request.prompt,
        "response": response
    }

# Keywords that indicate coding/AI related questions
ALLOWED_KEYWORDS = [
    "python", "code", "function", "algorithm", "programming",
    "machine learning", "AI", "deep learning", "neural network",
    "data", "model", "train", "dataset", "array", "list",
    "loop", "class", "object", "variable", "debug", "error",
    "library", "import", "install", "tensorflow", "pytorch",
    "numpy", "pandas", "scikit", "api", "server", "database",
    "sql", "javascript", "html", "css", "java", "c++", "git",
    "ml", "llm", "nlp", "computer vision"
]

def is_coding_related(message: str) -> bool:
    message_lower = message.lower()
    for keyword in ALLOWED_KEYWORDS:
        if ' ' in keyword:
            # Multi-word keyword — direct string match
            if keyword in message_lower:
                return True
        else:
            # Single word keyword — whole word match
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, message_lower):
                return True
    return False

@app.post("/chat")
def chat(request: ChatRequest):
    request_id = str(uuid.uuid4())
    logger.info(f"Request ID: {request_id} - /chat called")

    # Check if question is coding related
    last_message = request.messages[-1].content
    if not is_coding_related(last_message):
        return {
            "request_id": request_id,
            "response": "I'm sorry! I can only answer coding and AI/ML related questions.",
            "messages": []
        }

    model = get_model()

    messages = [{"role": "system", "content": request.system_prompt}]
    for msg in request.messages:
        messages.append({"role": msg.role, "content": msg.content})

    output = model.create_chat_completion(
        messages=messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_k=request.top_k,
        top_p=request.top_p
    )

    response = output['choices'][0]['message']['content']
    logger.info(f"Request ID: {request_id} - Response generated")

    return {
        "request_id": request_id,
        "response": response,
        "messages": messages
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)