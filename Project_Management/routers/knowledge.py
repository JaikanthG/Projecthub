# routers/knowledge.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..schemas import (
    CreateKnowledge,
    UpdateKnowledge
)

from ..services.knowledge_service import KnowledgeService


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Repository"]
)


# ============================================================
# CREATE KNOWLEDGE
# ============================================================

@router.post("/")
def create_knowledge(
    knowledge: CreateKnowledge,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    created_knowledge = KnowledgeService.create_knowledge(
        knowledge,
        current_user,
        db
    )

    return {
        "message": "Knowledge created successfully.",
        "data": created_knowledge
    }


# ============================================================
# GET ALL KNOWLEDGE
#
# IMPORTANT:
# project_id is REQUIRED.
#
# Example:
# GET /knowledge/?project_id=9
#
# This prevents loading knowledge from every project.
# ============================================================

@router.get("/")
def get_all_knowledge(
    project_id: int = Query(
        ...,
        description="Current project ID"
    ),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    knowledge = KnowledgeService.get_all_knowledge(
        project_id,
        db
    )

    return {
        "count": len(knowledge),
        "data": knowledge
    }


# ============================================================
# GET KNOWLEDGE BY ID
# ============================================================

@router.get("/{knowledge_id}")
def get_knowledge_by_id(
    knowledge_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return KnowledgeService.get_knowledge_by_id(
        knowledge_id,
        db
    )


# ============================================================
# UPDATE KNOWLEDGE
# ============================================================

@router.put("/{knowledge_id}")
def update_knowledge(
    knowledge_id: int,
    knowledge: UpdateKnowledge,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    updated_knowledge = KnowledgeService.update_knowledge(
        knowledge_id,
        knowledge,
        current_user,
        db
    )

    return {
        "message": "Knowledge updated successfully.",
        "data": updated_knowledge
    }


# ============================================================
# DELETE KNOWLEDGE
# ============================================================

@router.delete("/{knowledge_id}")
def delete_knowledge(
    knowledge_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return KnowledgeService.delete_knowledge(
        knowledge_id,
        current_user,
        db
    )