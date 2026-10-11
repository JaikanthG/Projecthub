# ============================================================
# PROJECT HUB RAG - VECTOR STORE
# ============================================================

from sqlalchemy.orm import Session

from ..models import KnowledgeChunk


# ============================================================
# DELETE EXISTING CHUNKS
# ============================================================

def delete_knowledge_chunks(
    knowledge_id: int,
    db: Session,
):
    """
    Delete existing chunks for a knowledge article.

    This allows re-indexing when the knowledge content changes.
    """

    db.query(
        KnowledgeChunk
    ).filter(
        KnowledgeChunk.knowledge_id == knowledge_id
    ).delete(
        synchronize_session=False
    )

    db.commit()


# ============================================================
# STORE CHUNKS
# ============================================================

def store_chunks(
    knowledge_id: int,
    project_id: int,
    chunks: list[str],
    embeddings: list[list[float]],
    db: Session,
):
    """
    Store chunks and their embeddings.
    """

    if len(chunks) != len(embeddings):

        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    records = []

    for index, (
        content,
        embedding
    ) in enumerate(
        zip(chunks, embeddings)
    ):

        record = KnowledgeChunk(

            knowledge_id=knowledge_id,

            project_id=project_id,

            chunk_index=index,

            content=content,

            embedding=embedding,
        )

        records.append(record)

    if records:

        db.add_all(records)

        db.commit()

        for record in records:
            db.refresh(record)

    return records