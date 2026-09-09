import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.query import router as query_router
from app.core.config import get_settings
from app.services.generation import GenerationService
from app.services.retrieval import RetrievalService
from app.utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: load the vector store and the LLM client ONCE (never per request)."""
    retrieval = RetrievalService()
    retrieval.load()
    app.state.retrieval = retrieval

    generation = GenerationService()
    app.state.generation = generation

    if retrieval.ready:
        logger.info("Retrieval service ready (%d chunks).", retrieval.collection.count())
    else:
        logger.warning(
            "Retrieval service NOT ready — run notebooks/rag_pipeline.ipynb to build the vector store."
        )

    if generation.check_connection():
        logger.info("Ollama reachable at %s (model '%s').",
                    settings.OLLAMA_BASE_URL, settings.OLLAMA_MODEL)
    else:
        logger.warning("Ollama not reachable at %s — start it with `ollama serve` and pull the model.",
                       settings.OLLAMA_BASE_URL)

    yield

    logger.info("Shutting down RAG Assistant API.")


app = FastAPI(
    title=settings.APP_NAME,
    description="FastAPI backend serving the Ollama & ChromaDB document assistant",
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Allowed frontend origin(s) — comma-separated in .env, e.g. http://localhost:8501
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router)


#uvicorn app.main:app --reload