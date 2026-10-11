# ============================================================
# PROJECT HUB - AGNO KNOWLEDGE
# ============================================================

import os


from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.ollama import OllamaEmbedder
from agno.knowledge.chunking.recursive import RecursiveChunking
from agno.knowledge.reader.text_reader import TextReader
from agno.vectordb.pgvector import PgVector
from agno.vectordb.search import SearchType


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:root@localhost:5432/project_management",
)


# ============================================================
# EMBEDDING
# ============================================================

embedder = OllamaEmbedder(
    id="nomic-embed-text",
    dimensions=768,
)


# ============================================================
# KNOWLEDGE
# ============================================================

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="projecthub_embeddings",
        db_url=DATABASE_URL,
        search_type=SearchType.hybrid,
        embedder=embedder,
    ),
    max_results=5,
)


# ============================================================
# READER
# ============================================================

reader = TextReader(
    chunking_strategy=RecursiveChunking(
        chunk_size=800,
        overlap=100,
    ),
)