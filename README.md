# RAG Support Desk Assistant

A Retrieval-Augmented Generation (RAG) Support Desk Assistant that answers customer-support questions using a collection of trusted PDF documents.

The system retrieves relevant information from the document knowledge base and provides grounded answers using a local Large Language Model (LLM). If the required information cannot be found in the available documents, the assistant avoids making up an answer and returns an appropriate fallback response.

---

## Overview

The RAG Support Desk Assistant is designed to provide reliable answers to common customer-support questions.

The application uses:

- **Streamlit** for the user interface
- **FastAPI** for the backend API
- **Sentence Transformers** for text embeddings
- **ChromaDB** for vector storage and similarity search
- **Ollama / Llama 3.2** for local response generation
- **PDF documents** as the knowledge base

The main goal is to ensure that generated answers are based on retrieved information from the provided documents rather than relying only on the LLM's general knowledge.

---

## Features

- 📚 PDF-based knowledge base
- 🔎 Semantic document retrieval
- 🤖 Local LLM-based answer generation
- 🛡️ Grounded responses using retrieved context
- ❌ Fallback response when information is unavailable
- 📄 Source information associated with retrieved documents
- 🚀 FastAPI backend
- 🖥️ Streamlit frontend
- 💾 Persistent ChromaDB vector store
- 🧪 Evaluation using predefined test questions

---

# Architecture

The application follows a Retrieval-Augmented Generation pipeline:

```text
                         User
                           │
                           ▼
                  ┌─────────────────┐
                  │ Streamlit UI    │
                  │    Frontend     │
                  └────────┬────────┘
                           │
                    HTTP POST /query
                           │
                           ▼
                  ┌─────────────────┐
                  │    FastAPI      │
                  │     Backend     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Retrieval       │
                  │ Service         │
                  └────────┬────────┘
                           │
                 Semantic Similarity
                           │
                           ▼
                  ┌─────────────────┐
                  │    ChromaDB     │
                  │  Vector Store   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Retrieved       │
                  │ Context         │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Generation      │
                  │ Service         │
                  │ Ollama / LLM    │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Grounded Answer │
                  │ + Sources       │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Streamlit UI    │
                  └─────────────────┘

```
## Setup

---

### Backend
```
bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
ollama pull llama3.2
uvicorn app.main:app --reload


### Frontend
bash
cd frontend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
