import logging

from fastapi import APIRouter, HTTPException, Request, status

from app.schemas.query import QueryRequest, QueryResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["query"])


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check(request: Request):
    """Liveness + readiness check for the backend."""
    retrieval = getattr(request.app.state, "retrieval", None)
    generation = getattr(request.app.state, "generation", None)

    return {
        "status": "ok",
        "message": "RAG Backend Service running successfully.",
        "vector_store_loaded": bool(retrieval and retrieval.ready),
        "ollama_reachable": bool(generation and generation.check_connection()),
    }


@router.post("/query", response_model=QueryResponse, status_code=status.HTTP_200_OK)
def process_query(payload: QueryRequest, request: Request):
    """Run the RAG pipeline: retrieve -> build prompt -> call LLM -> grounded answer."""
    retrieval = getattr(request.app.state, "retrieval", None)
    generation = getattr(request.app.state, "generation", None)

    if retrieval is None or not retrieval.ready:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector store is not loaded. Run notebooks/rag_pipeline.ipynb to build it first.",
        )
    if generation is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Generation service unavailable.",
        )

    try:
        chunks = retrieval.retrieve(payload.question)
        answer, sources = generation.generate(payload.question, chunks)
        return QueryResponse(answer=answer, sources=sources)
    except HTTPException:
        raise
    except Exception as err:
        logger.exception("RAG pipeline failed while answering a question.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG Execution Error: {err}",
        )