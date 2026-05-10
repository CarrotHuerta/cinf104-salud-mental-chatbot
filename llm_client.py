import requests


class OllamaClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")


def create_ollama_client(base_url):
    return OllamaClient(base_url=base_url)


def request_chat_completion(
    client,
    model,
    messages,
    temperature,
    max_tokens,
    top_p=None,
    repeat_penalty=None,
):
    options = {"temperature": temperature}
    if max_tokens is not None:
        options["num_predict"] = max_tokens
    if top_p is not None:
        options["top_p"] = top_p
    if repeat_penalty is not None:
        options["repeat_penalty"] = repeat_penalty

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": options,
    }

    response = requests.post(
        f"{client.base_url}/api/chat",
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]
