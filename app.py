import os
import shutil
import subprocess
import time

import requests

import streamlit as st

import config as cfg
from llm_client import create_ollama_client, request_chat_completion
from prompting import build_messages, load_system_prompt

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

@st.cache_data(show_spinner=False)
def get_system_prompt():
    return load_system_prompt()


def render_logo():
    logo_path = getattr(cfg, "LOGO_PATH", None)
    if logo_path:
        logo_path = str(logo_path)
    else:
        logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.svg")

    if not os.path.isfile(logo_path):
        return

    if hasattr(st, "logo"):
        st.logo(logo_path)
    else:
        st.image(logo_path, width=64)


def is_ollama_running(base_url):
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=2)
        return response.ok
    except requests.RequestException:
        return False


def can_run_ollama(ollama_exe):
    if not ollama_exe:
        return False
    if os.path.isfile(ollama_exe):
        return True
    return shutil.which(ollama_exe) is not None


def start_ollama(ollama_exe):
    if not can_run_ollama(ollama_exe):
        return False

    kwargs = {
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }
    if os.name == "nt":
        kwargs["creationflags"] = (
            subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        )

    subprocess.Popen([ollama_exe, "serve"], **kwargs)
    return True


def ensure_ollama_running(base_url, ollama_exe):
    if is_ollama_running(base_url):
        return True

    if not start_ollama(ollama_exe):
        return False

    for _ in range(10):
        time.sleep(0.5)
        if is_ollama_running(base_url):
            return True
    return False


def main():
    app_title = getattr(cfg, "APP_TITLE", "Chatbot de Apoyo Psicologico")
    app_caption = getattr(cfg, "APP_CAPTION", "")

    st.set_page_config(page_title=app_title, page_icon="💬")
    render_logo()
    st.title(app_title)
    st.caption(app_caption)

    try:
        system_prompt = get_system_prompt()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.stop()

    with st.sidebar:
        st.header("Configuracion")
        st.caption("Modo local con Ollama (sin API key).")

    base_url = os.getenv(
        "OLLAMA_BASE_URL",
        getattr(cfg, "DEFAULT_BASE_URL", "http://localhost:11434"),
    ).strip()
    model = os.getenv(
        "OLLAMA_MODEL",
        getattr(cfg, "DEFAULT_MODEL", "llama3.2:1b"),
    ).strip()
    ollama_exe = os.getenv(
        "OLLAMA_EXE",
        getattr(cfg, "DEFAULT_OLLAMA_EXE", "ollama"),
    ).strip()

    temperature = getattr(cfg, "TEMPERATURE", 0.2)
    max_tokens = getattr(cfg, "MAX_TOKENS", 400)
    top_p = getattr(cfg, "TOP_P", 0.9)
    repeat_penalty = getattr(cfg, "REPEAT_PENALTY", 1.1)

    if not base_url or not model:
        st.error("Configura OLLAMA_BASE_URL y OLLAMA_MODEL en .env si es necesario.")
        st.stop()

    with st.sidebar:
        st.write(f"Base URL: {base_url}")
        st.write(f"Modelo fijo: {model}")
        st.write(f"Ollama exe: {ollama_exe}")

    if not is_ollama_running(base_url):
        with st.spinner("Iniciando Ollama local..."):
            ok = ensure_ollama_running(base_url, ollama_exe)
        if not ok:
            st.error(
                "No se pudo iniciar Ollama automaticamente. "
                "Ejecuta 'ollama serve' o revisa OLLAMA_EXE."
            )
            st.stop()

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hola, estoy aqui para escucharte. ¿En que te puedo apoyar hoy?",
            }
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Escribe tu mensaje...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                # Conexion y solicitud al LLM usando Ollama local
                client = create_ollama_client(base_url=base_url)
                try:
                    messages = build_messages(st.session_state.messages, system_prompt)
                    assistant_text = request_chat_completion(
                        client,
                        model=model,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        top_p=top_p,
                        repeat_penalty=repeat_penalty,
                    )
                    st.write(assistant_text)
                except Exception:
                    assistant_text = (
                        "Lo siento, hubo un error con el modelo local. "
                        "Intenta nuevamente en unos segundos."
                    )
                    st.error(
                        "No se pudo conectar a Ollama. Verifica que este corriendo."
                    )

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_text}
        )


if __name__ == "__main__":
    main()
