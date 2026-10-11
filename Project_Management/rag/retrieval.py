# ============================================================
# PROJECT HUB RAG - RETRIEVAL
# ============================================================

from sqlalchemy.orm import Session

from ..models import KnowledgeChunk

from .embeddings import create_embedding


# ============================================================
# SEARCH KNOWLEDGE
# ============================================================

def search_knowledge(
    query: str,
    db: Session,
    project_id: int | None = None,
    top_k: int = 5,
):
    """
    Search Project Hub knowledge using pgvector similarity.
    """

    if not query or not query.strip():

        return []

    if top_k <= 0:

        raise ValueError(
            "top_k must be greater than 0."
        )

    # --------------------------------------------------------
    # Convert query to embedding
    # --------------------------------------------------------

    query_embedding = create_embedding(
        query
    )

    # --------------------------------------------------------
    # Base query
    # --------------------------------------------------------

    similarity_query = (
        db.query(
            KnowledgeChunk
        )
    )

    # --------------------------------------------------------
    # Project filter
    # --------------------------------------------------------

    if project_id is not None:

        similarity_query = similarity_query.filter(
            KnowledgeChunk.project_id == project_id
        )

    # --------------------------------------------------------
    # Vector similarity
    #
    # cosine_distance:
    #
    # lower = more similar
    # --------------------------------------------------------

    similarity_query = (
        similarity_query
        .order_by(
            KnowledgeChunk.embedding.cosine_distance(
                query_embedding
            )
        )
        .limit(top_k)
    )

    return similarity_query.all()


# ============================================================
# SEARCH AND RETURN TEXT
# ============================================================

def retrieve_context(
    query: str,
    db: Session,
    project_id: int | None = None,
    top_k: int = 5,
):
    """
    Return only the relevant text chunks.
    """

    chunks = search_knowledge(
        query=query,
        db=db,
        project_id=project_id,
        top_k=top_k,
    )

    return [
        chunk.content
        for chunk in chunks
    ]