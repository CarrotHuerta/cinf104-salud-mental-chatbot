from config import PROMPT_PATH


def load_system_prompt():
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(
            "No se encontro el prompt. Crea prompts/system_prompt.txt"
        )
    return PROMPT_PATH.read_text(encoding="utf-8")


def build_messages(history, system_prompt):
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    return messages
