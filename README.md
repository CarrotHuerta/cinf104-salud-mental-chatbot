CINF104 Proyecto 1 - Chatbot PAP (Local)

Resumen
- Chatbot de Primeros Auxilios Psicologicos (PAP) con IA local via Ollama.
- No requiere API key.
- Incluye auto-inicio de Ollama y logo.

Requisitos
- Windows 10/11.
- Python 3.10+.
- PowerShell.
- Winget (recomendado para instalar Ollama automaticamente).

Inicio rapido (Windows)
1) Abre PowerShell en esta carpeta.
2) Ejecuta:
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\run.ps1
3) Abre el navegador en:
  http://localhost:8501

Que hace run.ps1
- Crea .venv si no existe.
- Instala dependencias Python.
- Instala Ollama con winget si no existe.
- Descarga el modelo local.
- Inicia la app Streamlit.

Ejecucion manual
1) Crear venv:
  python -m venv .venv
2) Activar venv:
  .\.venv\Scripts\Activate.ps1
3) Instalar deps:
  pip install -r requirements.txt
4) Instalar Ollama:
  winget install -e --id Ollama.Ollama
5) Descargar modelo:
  ollama pull llama3.2:1b
6) Ejecutar app:
  streamlit run app.py

Configuracion (.env)
- Copia .env.example a .env y ajusta:
  OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_EXE
- Si cambias el modelo, ejecuta:
  ollama pull <modelo>

Solucion de problemas
- Si dice que Ollama no corre, ejecuta: ollama serve
- Si winget no existe, instala Ollama desde https://ollama.com
- Si el puerto 8501 esta ocupado, usa:
  streamlit run app.py --server.port 8502

Estructura
- app.py (UI Streamlit)
- config.py (parametros)
- llm_client.py (cliente Ollama)
- prompts/system_prompt.txt (prompt)
- assets/logo.svg (logo)
- run.ps1 (auto-instalacion y ejecucion)
