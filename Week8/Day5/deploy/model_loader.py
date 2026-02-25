import logging
from llama_cpp import Llama
from deploy.config import MODEL_PATH, MAX_TOKENS

# Setup logging
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

# Global model variable
model = None

def load_model():
    global model
    if model is None:
        logger.info("Loading GGUF model...")
        model = Llama(
            model_path=MODEL_PATH,
            n_gpu_layers=-1,  # use GPU if available
            n_ctx=2048,       # context window
            verbose=False
        )
        logger.info("Model loaded successfully!")
    return model

def get_model():
    global model
    if model is None:
        load_model()
    return model