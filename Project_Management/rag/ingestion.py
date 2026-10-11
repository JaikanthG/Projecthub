# ============================================================
# PROJECT HUB RAG - AGNO INGESTION
# ============================================================

from pathlib import Path

from sqlalchemy.orm import Session

from ..models import Knowledge, Document

from .agno_knowledge import knowledge as agno_knowledge
from .agno_knowledge import reader


# ============================================================
# INGEST ONE KNOWLEDGE ARTICLE
# ============================================================

def ingest_knowledge(
    knowledge_id: int,
    db: Session,
):
    """
    Index one Project Hub knowledge article using Agno.

    Pipeline:

        Project Hub Knowledge
                ↓
        RecursiveChunking
                ↓
        Ollama nomic-embed-text
                ↓
        768-dimensional embeddings
                ↓
        PostgreSQL + pgvector
    """

    # --------------------------------------------------------
    # Find Knowledge record
    # --------------------------------------------------------

    knowledge_record = (
        db.query(Knowledge)
        .filter(
            Knowledge.id == knowledge_id
        )
        .first()
    )

    if knowledge_record is None:

        raise ValueError(
            f"Knowledge with id {knowledge_id} not found."
        )

    if not knowledge_record.content:

        raise ValueError(
            "Knowledge content is empty."
        )

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    metadata = {
        "knowledge_id": knowledge_record.id,
        "project_id": knowledge_record.project_id,
        "title": knowledge_record.title,
    }

    # --------------------------------------------------------
    # Delete previous Agno vectors
    # --------------------------------------------------------

    agno_knowledge.vector_db.delete_by_metadata(
        metadata={
            "knowledge_id": knowledge_record.id
        }
    )

    # --------------------------------------------------------
    # Agno Knowledge ingestion
    # --------------------------------------------------------

    agno_knowledge.insert(
        name=knowledge_record.title,
        text_content=knowledge_record.content,
        reader=reader,
        metadata=metadata,
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "knowledge_id": knowledge_record.id,
        "project_id": knowledge_record.project_id,
        "title": knowledge_record.title,
        "status": "indexed",
    }


# ============================================================
# INGEST ALL PUBLISHED KNOWLEDGE
# ============================================================

def ingest_all_knowledge(
    db: Session,
):
    """
    Index all published Project Hub knowledge articles
    using Agno Knowledge.
    """

    knowledge_items = (
        db.query(Knowledge)
        .filter(
            Knowledge.status == "published"
        )
        .all()
    )

    results = []

    for knowledge_record in knowledge_items:

        try:

            result = ingest_knowledge(
                knowledge_id=knowledge_record.id,
                db=db,
            )

            results.append(
                result
            )

        except Exception as exc:

            db.rollback()

            results.append({
                "knowledge_id": knowledge_record.id,
                "project_id": knowledge_record.project_id,
                "title": knowledge_record.title,
                "status": "failed",
                "error": str(exc),
            })

    return results


# ============================================================
# READ TEXT DOCUMENT
# ============================================================

def read_document_text(
    file_path: str,
) -> str:
    """
    Read a text-based Project Hub document.

    Supported:
        .txt
        .md
    """

    if not file_path:

        raise ValueError(
            "Document file path is empty."
        )

    path = Path(
        file_path
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Document file not found: {file_path}"
        )

    extension = path.suffix.lower()

    supported_extensions = {
        ".txt",
        ".md",
    }

    if extension not in supported_extensions:

        raise ValueError(
            f"Unsupported RAG document type: {extension}. "
            "Currently supported: .txt and .md."
        )

    try:

        return path.read_text(
            encoding="utf-8"
        )

    except UnicodeDecodeError as exc:

        raise ValueError(
            f"Unable to decode document as UTF-8: {file_path}"
        ) from exc


# ============================================================
# INGEST ONE UPLOADED DOCUMENT
# ============================================================

def ingest_document(
    document_id: int,
    db: Session,
):
    """
    Process one uploaded Project Hub document.

    Pipeline:

        Document
            ↓
        Read file
            ↓
        Create / update Knowledge record
            ↓
        Agno Knowledge
            ↓
        RecursiveChunking
            ↓
        Ollama Embedding
            ↓
        PgVector
    """

    # --------------------------------------------------------
    # Find document
    # --------------------------------------------------------

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if document is None:

        raise ValueError(
            f"Document with id {document_id} not found."
        )

    # --------------------------------------------------------
    # Capture document values
    # --------------------------------------------------------

    document_id_value = document.id
    document_name = document.file_name
    document_project_id = document.project_id
    document_uploaded_by = document.uploaded_by
    document_file_path = document.file_path

    # --------------------------------------------------------
    # Read uploaded file
    # --------------------------------------------------------

    content = read_document_text(
        document_file_path
    )

    if not content.strip():

        raise ValueError(
            "Document content is empty."
        )

    # --------------------------------------------------------
    # Create / find Knowledge record
    # --------------------------------------------------------

    title = Path(
        document_name
    ).stem

    existing_knowledge = (
        db.query(Knowledge)
        .filter(
            Knowledge.project_id == document_project_id,
            Knowledge.title == title,
        )
        .first()
    )

    if existing_knowledge:

        # ----------------------------------------------------
        # Update existing Knowledge
        # ----------------------------------------------------

        knowledge_record = existing_knowledge

        knowledge_record.content = content

        knowledge_record.status = "published"

        if knowledge_record.tags is None:

            knowledge_record.tags = ""

    else:

        # ----------------------------------------------------
        # Create new Knowledge
        # ----------------------------------------------------

        knowledge_record = Knowledge(

            project_id=document_project_id,

            title=title,

            content=content,

            tags="",

            status="published",

            created_by=document_uploaded_by,

        )

        db.add(
            knowledge_record
        )

    # --------------------------------------------------------
    # Save Knowledge record
    # --------------------------------------------------------

    try:

        db.commit()

    except Exception:

        db.rollback()

        raise

    db.refresh(
        knowledge_record
    )

    # --------------------------------------------------------
    # Index Knowledge using Agno
    # --------------------------------------------------------

    result = ingest_knowledge(
        knowledge_id=knowledge_record.id,
        db=db,
    )

    # --------------------------------------------------------
    # Add document information
    # --------------------------------------------------------

    result.update({

        "document_id": document_id_value,

        "document_name": document_name,

    })

    return result


# ============================================================
# INGEST ALL UPLOADED TEXT DOCUMENTS
# ============================================================

def ingest_all_documents(
    db: Session,
    project_id: int | None = None,
):
    """
    Ingest uploaded Project Hub text/Markdown documents.

    If project_id is provided, only documents belonging
    to that project are processed.
    """

    query = (
        db.query(Document)
    )

    # --------------------------------------------------------
    # Optional project filter
    # --------------------------------------------------------

    if project_id is not None:

        query = query.filter(
            Document.project_id == project_id
        )

    documents = query.all()

    results = []

    for document in documents:

        document_id = document.id

        document_name = document.file_name

        document_project_id = document.project_id

        try:

            result = ingest_document(
                document_id=document_id,
                db=db,
            )

            results.append(
                result
            )

        except Exception as exc:

            db.rollback()

            results.append({

                "document_id": document_id,

                "document_name": document_name,

                "project_id": document_project_id,

                "status": "failed",

                "error": str(exc),

            })

    return results