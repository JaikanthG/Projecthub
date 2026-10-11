from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Knowledge

from ..repositories.knowledge_repository import (
    KnowledgeRepository
)

from ..repositories.activity_repository import (
    ActivityRepository
)

from ..utils.permissions import (
    require_admin,
    require_contributor_or_admin
)

from ..rag.ingestion import ingest_knowledge


class KnowledgeService:

    # ==========================================
    # Create Knowledge
    # ==========================================

    @staticmethod
    def create_knowledge(
        knowledge,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Admin OR Contributor
        # ==========================================

        require_contributor_or_admin(
            knowledge.project_id,
            current_user,
            db
        )

        # ==========================================
        # Check Duplicate
        # ==========================================

        existing_knowledge = (
            KnowledgeRepository.get_knowledge_by_title(
                knowledge.title,
                db
            )
        )

        if existing_knowledge:

            raise HTTPException(
                status_code=400,
                detail="Knowledge title already exists."
            )

        # ==========================================
        # Create Knowledge
        # ==========================================

        new_knowledge = Knowledge(
            project_id=knowledge.project_id,
            title=knowledge.title,
            content=knowledge.content,
            tags=knowledge.tags.lower(),
            version=knowledge.version,
            status=knowledge.status.lower(),
            created_by=current_user["user_id"]
        )

        created_knowledge = (
            KnowledgeRepository.create_knowledge(
                new_knowledge,
                db
            )
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=created_knowledge.project_id,
            user_id=current_user["user_id"],
            action="CREATE",
            entity_type="KNOWLEDGE",
            entity_id=created_knowledge.id,
            description=(
                f"Created knowledge: "
                f"{created_knowledge.title}"
            ),
            db=db
        )

        # ==========================================
        # RAG INGESTION
        # ==========================================
        #
        # Only published knowledge should be
        # inserted into the AI knowledge base.
        #
        # The ingestion function adds:
        #
        #   knowledge_id
        #   project_id
        #   title
        #
        # to Agno metadata.
        # ==========================================

        if created_knowledge.status == "published":

            try:

                ingest_knowledge(
                    knowledge_id=created_knowledge.id,
                    db=db
                )

            except Exception as exc:

                # ----------------------------------
                # Knowledge was created, but RAG
                # indexing failed.
                # ----------------------------------

                raise HTTPException(
                    status_code=500,
                    detail=(
                        "Knowledge was created successfully, "
                        "but RAG indexing failed: "
                        f"{str(exc)}"
                    )
                ) from exc

        return created_knowledge


    # ==========================================
    # Get All Knowledge
    # ==========================================

    @staticmethod
    def get_all_knowledge(
        project_id: int,
        db: Session
    ):

        # ==========================================
        # PROJECT-SCOPED KNOWLEDGE
        # ==========================================

        knowledge_items = (
            db.query(Knowledge)
            .filter(
                Knowledge.project_id == project_id
            )
            .order_by(
                Knowledge.id.asc()
            )
            .all()
        )

        return knowledge_items


    # ==========================================
    # Get Knowledge By ID
    # ==========================================

    @staticmethod
    def get_knowledge_by_id(
        knowledge_id: int,
        db: Session
    ):

        knowledge = (
            KnowledgeRepository.get_knowledge_by_id(
                knowledge_id,
                db
            )
        )

        if knowledge is None:

            raise HTTPException(
                status_code=404,
                detail="Knowledge not found."
            )

        return knowledge


    # ==========================================
    # Update Knowledge
    # ==========================================

    @staticmethod
    def update_knowledge(
        knowledge_id: int,
        updated_knowledge,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Get Knowledge
        # ==========================================

        knowledge = (
            KnowledgeRepository.get_knowledge_by_id(
                knowledge_id,
                db
            )
        )

        if knowledge is None:

            raise HTTPException(
                status_code=404,
                detail="Knowledge not found."
            )

        # ==========================================
        # Admin OR Contributor
        # ==========================================

        require_contributor_or_admin(
            knowledge.project_id,
            current_user,
            db
        )

        # ==========================================
        # Check Duplicate Title
        # ==========================================

        duplicate = (
            KnowledgeRepository.get_knowledge_by_title(
                updated_knowledge.title,
                db
            )
        )

        if (
            duplicate
            and duplicate.id != knowledge_id
        ):

            raise HTTPException(
                status_code=400,
                detail="Knowledge title already exists."
            )

        # ==========================================
        # Update Knowledge
        # ==========================================

        knowledge.title = (
            updated_knowledge.title
        )

        knowledge.content = (
            updated_knowledge.content
        )

        knowledge.tags = (
            updated_knowledge.tags.lower()
        )

        knowledge.version = (
            updated_knowledge.version
        )

        knowledge.status = (
            updated_knowledge.status.lower()
        )

        KnowledgeRepository.update_knowledge(
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=knowledge.project_id,
            user_id=current_user["user_id"],
            action="UPDATE",
            entity_type="KNOWLEDGE",
            entity_id=knowledge.id,
            description=(
                f"Updated knowledge: "
                f"{knowledge.title}"
            ),
            db=db
        )

        return knowledge


    # ==========================================
    # Delete Knowledge
    # ==========================================

    @staticmethod
    def delete_knowledge(
        knowledge_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Get Knowledge
        # ==========================================

        knowledge = (
            KnowledgeRepository.get_knowledge_by_id(
                knowledge_id,
                db
            )
        )

        if knowledge is None:

            raise HTTPException(
                status_code=404,
                detail="Knowledge not found."
            )

        # ==========================================
        # ONLY ADMIN CAN DELETE
        # ==========================================

        require_admin(
            current_user
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=knowledge.project_id,
            user_id=current_user["user_id"],
            action="DELETE",
            entity_type="KNOWLEDGE",
            entity_id=knowledge.id,
            description=(
                f"Deleted knowledge: "
                f"{knowledge.title}"
            ),
            db=db
        )

        # ==========================================
        # Delete Knowledge
        # ==========================================

        KnowledgeRepository.delete_knowledge(
            knowledge,
            db
        )

        return {
            "message": "Knowledge deleted successfully."
        }