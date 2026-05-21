from pathlib import Path

# =====================================================================
# PATH CONFIGURATION
# =====================================================================

PARENT_DIR = Path(__file__).resolve().parent.parent

#Define where our images are store

IMAGE_DIR = PARENT_DIR / "test_images"
REPORT_DIR = PARENT_DIR / "reports"
REPORT_PATH= REPORT_DIR /"report.md"

# =====================================================================
# VLM MODEL CONFIGURATION
# =====================================================================
# The active model name running in Ollama
VLM_MODEL_NAME = "llava:7b"

# The local Ollama server address
OLLAMA_API_BASE_URL = "http://localhost:11434"

ENDPOINT_GENERATE = "/api/generate"



# =====================================================================
# VALIDATION PARAMETERS
# =====================================================================
# The default confidence score threshold we accept from the VLM
MINIMUM_CONFIDENCE_SCORE = 0.8
