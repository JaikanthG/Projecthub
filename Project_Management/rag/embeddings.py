# ============================================================
# PROJECT HUB RAG - EMBEDDINGS
# ============================================================

from functools import lru_cache

import ollama


# ------------------------------------------------------------
# Model Configuration
# ------------------------------------------------------------

EMBEDDING_MODEL = "nomic-embed-text"

EMBEDDING_DIMENSION = 768


# ------------------------------------------------------------
# Load / Configure Ollama
# ------------------------------------------------------------

@lru_cache(maxsize=1)
def get_embedding_model():

    return EMBEDDING_MODEL


# ------------------------------------------------------------
# Single Text Embedding
# ------------------------------------------------------------

def create_embedding(
    text: str
) -> list[float]:

    if not text or not text.strip():

        raise ValueError(
            "Cannot create embedding for empty text."
        )

    model = get_embedding_model()

    response = ollama.embed(
        model=model,
        input=text.strip()
    )

    embedding = response["embeddings"][0]

    return embedding


# ------------------------------------------------------------
# Multiple Text Embeddings
# ------------------------------------------------------------

def create_embeddings(
    texts: list[str]
) -> list[list[float]]:

    if not texts:
        return []

    cleaned_texts = [
        text.strip()
        for text in texts
        if text and text.strip()
    ]

    if not cleaned_texts:
        return []

    model = get_embedding_model()

    response = ollama.embed(
        model=model,
        input=cleaned_texts
    )

    return response["embeddings"]