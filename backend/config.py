"""Configuration for the LLM Council."""

import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Logging configuration
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "council.log")

# Create logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# LM Studio Configuration
# LM Studio provides an OpenAI-compatible API at http://localhost:1234/v1
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")

# Note: LM Studio typically doesn't require an API key for local usage
# But we keep this for compatibility if you set up authentication
LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "lm-studio")

# Council members - These are model names loaded in LM Studio
# You need to have these models loaded in LM Studio
# The model names should match what's shown in LM Studio's model list
# Default to generic names that you should customize based on your loaded models
COUNCIL_MODELS = os.getenv("COUNCIL_MODELS", "model-1,model-2,model-3").split(",")

# If you have specific models loaded, update this list:
# For example:
# COUNCIL_MODELS = [
#     "mistral-7b-instruct",
#     "llama-2-13b-chat", 
#     "neural-chat-7b",
# ]

# Chairman model - synthesizes final response
# This should also be a model loaded in LM Studio
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", COUNCIL_MODELS[0] if COUNCIL_MODELS else "model-1")

# LM Studio API endpoint (OpenAI-compatible)
LM_STUDIO_API_URL = f"{LM_STUDIO_BASE_URL}/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

logger.info(f"LM Studio configured at: {LM_STUDIO_BASE_URL}")
logger.info(f"Council models: {COUNCIL_MODELS}")
logger.info(f"Chairman model: {CHAIRMAN_MODEL}")
