import logging
from typing import Any, Dict, List, Optional

import chromadb
from sentence_transformers import SentenceTransformer

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class RetrievalService:
    """Loads the persisted ChromaDB store + embedding model once at startup,
    then answers similarity queries with cited chunks."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.embedding_model: Optional[SentenceTransformer] = None
        self.collection = None
        self.ready = False

    def load(self) -> bool:
        """Load the embedding model and the persisted collection.

        Returns True when the service is usable, False otherwise (the API
        still starts so /health can report the problem).
        """
        try:
            logger.info("Loading embedding model '%s'...", self.settings.EMBEDDING_MODEL_NAME)
            self.embedding_model = SentenceTransformer(self.settings.EMBEDDING_MODEL_NAME)

            client = chromadb.PersistentClient(path=self.settings.VECTOR_STORE_DIR)
            self.collection = client.get_collection(self.settings.COLLECTION_NAME)
            logger.info(
                "Loaded %d chunks from collection '%s' in %s",
                self.collection.count(),
                self.settings.COLLECTION_NAME,
                self.settings.VECTOR_STORE_DIR,
            )
            self.ready = True
        except Exception as exc:
            logger.error("Could not load the vector store: %s", exc)
            self.ready = False
        return self.ready

    def retrieve(self, question: str, top_k: Optional[int] = None) -> List[Dict[str, Any]]:
        """Embed the question and return the top-k most similar chunks."""
        if not self.ready:
            raise RuntimeError("Retrieval service is not loaded.")

        k = top_k or self.settings.TOP_K
        query_embedding = self.embedding_model.encode([question]).tolist()
        results = self.collection.query(query_embeddings=query_embedding, n_results=k)

        retrieved: List[Dict[str, Any]] = []
        for i in range(len(results["ids"][0])):
            retrieved.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })
        return retrieved