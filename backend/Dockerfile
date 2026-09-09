FROM python:3.10-slim

WORKDIR /code

# Dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY app ./app
COPY tests ./tests
COPY pytest.ini .

# Persisted vector store produced by notebooks/rag_pipeline.ipynb
# (run the notebook BEFORE docker build, or mount it at runtime)
COPY data ./data

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Ollama runs on the host — point OLLAMA_BASE_URL at it, e.g. on Docker Desktop:
#   docker run -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -p 8000:8000 rag-assistant-backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]