RAG Support Desk Assistant
A Retrieval-Augmented Generation (RAG) assistant for e-commerce customer support.Ask questions in plain language about products, orders, payments, shipping, returns,and account management — the system retrieves the relevant passages from the knowledgebase and generates a grounded answer with a local LLM (no external API keys).

Features
🔍 Semantic retrieval — ChromaDB vector store, persisted locally
🤖 Local generation — Ollama serves the LLM (e.g. llama3.1, mistral)
⚡ FastAPI backend — models & vector store loaded once at startup (lifespan)
🖥️ Streamlit chat UI — lightweight conversational frontend
📓 Reproducible pipeline — Jupyter notebook builds & evaluates the index
Architecture
Streamlit (frontend/app.py)        │  HTTP POST /query        ▼FastAPI (backend/app)        │        ├── RetrievalService ───► ChromaDB (backend/data/vector_store)        │        └── GenerationService ──► Ollama (local LLM)
Pipeline: PDFs → chunking → embeddings → ChromaDB → top-k retrieval → grounded prompt → LLM → answer

Project Structure
rag-assistant-project/├── data/raw_documents/        # source PDFs (knowledge base) — see its README├── notebooks/│   └── rag_pipeline.ipynb     # Phase 2 — chunk, embed, index, evaluate├── backend/│   ├── app/│   │   ├── main.py            # FastAPI app, CORS, lifespan startup│   │   ├── api/routes/        # GET /health, POST /query│   │   ├── core/config.py     # settings from .env│   │   ├── schemas/           # request/response models│   │   ├── services/          # retrieval.py, generation.py│   │   └── utils/             # logging│   ├── data/vector_store/     # persisted ChromaDB (built by the notebook)│   ├── tests/                 # pytest suite│   ├── requirements.txt│   ├── .env.example│   └── Dockerfile└── frontend/    ├── app.py                 # Streamlit chat UI    ├── api_client.py          # backend API wrapper    ├── requirements.txt    └── .env.example
Prerequisites
Python 3.10+
Ollama installed → https://ollama.com
Setup
1. Clone & install dependencies
git clone <repo-url>cd rag-assistant-project# backendcd backendpython -m venv .venv.venv\Scripts\activate          # Windowspip install -r requirements.txt# frontend (new terminal)cd frontendpip install -r requirements.txt# notebook / Phase-2 dependencies (project root)pip install -r requirements.txt
2. Configure environment
# backend — from backend/Copy-Item .env.example .env     # then set OLLAMA_MODEL, CORS_ORIGINS, ...# frontend — from frontend/Copy-Item .env.example .env     # set API_BASE_URL=http://localhost:8000
3. Start Ollama & pull a model
ollama serve                    # usually already running on Windowsollama pull llama3.1            # or the model set in backend/.env
4. Build the vector store
Open and run notebooks/rag_pipeline.ipynb end-to-end. It ingests the PDFs fromdata/raw_documents/, chunks & embeds them, and persists the index tobackend/data/vector_store/.

⚠️ The API will log Retrieval service NOT ready until this step is done once.

Running
Terminal 1 — backend (must stay open):

cd backend uvicorn app.main:app --reload
Run this from inside backend/ — the app package is resolved relative to it.Interactive API docs: http://localhost:8000/docs

Terminal 2 — frontend (must stay open):

cd frontend streamlit run app.py

API Endpoints
Method	Path	Description
GET	/health	Service status (retrieval & Ollama ready)
POST	/query	Ask a question → grounded answer + sources
Example:

curl -X POST http://localhost:8000/query ^  -H "Content-Type: application/json" ^  -d "{\"question\": \"How do I return a damaged item?\"}"
Testing
cd backendpytest
Troubleshooting
Symptom	Fix
ModuleNotFoundError: No module named 'app'	Run uvicorn app.main:app --reload from inside backend/, not the repo root
Frontend: "API_BASE_URL is not set" / "Assistant is offline"	Create frontend/.env (Step 2), then restart Streamlit — env vars are read at startup
Backend logs "Ollama not reachable"	Start Ollama (ollama serve) and confirm the model is pulled (ollama list)
Backend logs "Retrieval service NOT ready"	Run notebooks/rag_pipeline.ipynb to build the vector store