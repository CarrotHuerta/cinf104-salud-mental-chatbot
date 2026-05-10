import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.txt"
LOGO_PATH = BASE_DIR / "assets" / "logo.svg"

APP_TITLE = "Chatbot de Apoyo Psicologico"
APP_CAPTION = "Estoy aqui para ayudarte. Cuentame lo que te preocupa y hare lo posible por apoyarte."

DEFAULT_MODEL = "llama3.2:1b"
DEFAULT_BASE_URL = "http://localhost:11434"
_local_appdata = os.environ.get("LOCALAPPDATA", "")
if _local_appdata:
    DEFAULT_OLLAMA_EXE = str(
        Path(_local_appdata) / "Programs" / "Ollama" / "ollama.exe"
    )
else:
    DEFAULT_OLLAMA_EXE = "ollama"

TEMPERATURE = 0.2
TOP_P = 0.9
REPEAT_PENALTY = 1.1
MAX_TOKENS = 400
