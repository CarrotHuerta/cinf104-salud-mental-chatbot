CINF104 Proyecto 1 - Chatbot PAP (Local)

Quick start (Windows):
1) Open PowerShell in this folder.
2) Run:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\run.ps1

What run.ps1 does:
- Creates .venv if missing
- Installs Python dependencies
- Installs Ollama with winget if missing
- Pulls the local model
- Starts the Streamlit app

Manual run:
  .\.venv\Scripts\python.exe -m streamlit run app.py

Config:
- Copy .env.example to .env to override:
  OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_EXE
