from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    Query
)

from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from ..database import get_db
from ..auth import get_current_user

from ..services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# ==========================================
# Upload Document
# ==========================================

@router.post("/upload")
def upload_document(
    project_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    document = DocumentService.upload_document(
        project_id,
        file,
        current_user,
        db
    )

    return {
        "message": "Document uploaded successfully.",
        "data": document
    }


# ==========================================
# Get All Documents
# ==========================================

@router.get("/")
def get_documents(
    project_id: int = Query(
        ...,
        description="Current project ID"
    ),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    documents = DocumentService.get_documents(
        project_id,
        current_user,
        db
    )

    return {
        "count": len(documents),
        "data": documents
    }


# ==========================================
# Get Document By ID
# ==========================================

@router.get("/{document_id}")
def get_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return DocumentService.get_document(
        document_id,
        current_user,
        db
    )


# ==========================================
# Download Document
# ==========================================

@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    document = DocumentService.get_document(
        document_id,
        current_user,
        db
    )

    return FileResponse(
        path=document.file_path,
        filename=document.file_name,
        media_type="application/octet-stream"
    )


# ==========================================
# Get Documents By Project
# ==========================================

@router.get("/project/{project_id}")
def get_project_documents(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    documents = DocumentService.get_project_documents(
        project_id,
        current_user,
        db
    )

    return {
        "count": len(documents),
        "data": documents
    }


# ==========================================
# Delete Document
# ==========================================

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return DocumentService.delete_document(
        document_id,
        current_user,
        db
    )