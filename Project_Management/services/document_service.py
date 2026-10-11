from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from ..models import ProjectMember

from ..repositories.document_repository import (
    DocumentRepository
)

from ..repositories.activity_repository import (
    ActivityRepository
)

from ..utils.permissions import (
    require_admin,
    require_contributor_or_admin
)


class DocumentService:

    # ==========================================
    # Internal Project Access Check
    # ==========================================

    @staticmethod
    def _require_project_access(
        project_id: int,
        current_user: dict,
        db: Session
    ):
        """
        Project-level READ access.

        Admin:
            Full access to every project.

        Contributor:
            Can view documents in assigned projects.

        Member:
            Can view documents in assigned projects.

        Non-member:
            Denied.
        """

        # ------------------------------------------
        # Global Admin
        # ------------------------------------------

        if current_user["role"].lower() == "admin":
            return

        # ------------------------------------------
        # Check Project Membership
        # ------------------------------------------

        member = (
            db.query(ProjectMember)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == current_user["user_id"]
            )
            .first()
        )

        if member is None:

            raise HTTPException(
                status_code=403,
                detail="You are not a member of this project."
            )

    # ==========================================
    # Upload Document
    # ==========================================

    @staticmethod
    def upload_document(
        project_id: int,
        file: UploadFile,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # RBAC
        #
        # Admin                  -> Allowed
        # Employee + Contributor -> Allowed
        # Employee + Member      -> Denied
        # ==========================================

        require_contributor_or_admin(
            project_id,
            current_user,
            db
        )

        # ==========================================
        # Allowed File Extensions
        # ==========================================

        allowed_extensions = [
            "pdf",
            "doc",
            "docx",
            "txt",
            "md",
            "png",
            "jpg",
            "jpeg",
            "xlsx",
            "xls",
            "ppt",
            "pptx",
            "zip"
        ]

        # ==========================================
        # Validate Filename
        # ==========================================

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="File name is required."
            )

        # ==========================================
        # Validate Extension Exists
        # ==========================================

        if "." not in file.filename:

            raise HTTPException(
                status_code=400,
                detail="File must have an extension."
            )

        # ==========================================
        # Get Extension
        # ==========================================

        extension = (
            file.filename
            .rsplit(
                ".",
                1
            )[1]
            .lower()
        )

        # ==========================================
        # Validate Extension
        # ==========================================

        if extension not in allowed_extensions:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported file type. "
                    "Allowed types: "
                    + ", ".join(
                        allowed_extensions
                    )
                )
            )

        # ==========================================
        # Upload Document
        # ==========================================

        document = DocumentRepository.upload_document(
            project_id,
            file,
            current_user,
            db
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=document.project_id,
            user_id=current_user["user_id"],
            action="UPLOAD",
            entity_type="DOCUMENT",
            entity_id=document.id,
            description=(
                f"Uploaded document: "
                f"{document.file_name}"
            ),
            db=db
        )

        return document

    # ==========================================
    # Get All Documents For Project
    # ==========================================

    @staticmethod
    def get_documents(
        project_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Project-Level READ Access
        # ==========================================

        DocumentService._require_project_access(
            project_id,
            current_user,
            db
        )

        # ==========================================
        # Get Project Documents
        # ==========================================

        return DocumentRepository.get_project_documents(
            project_id,
            db
        )

    # ==========================================
    # Get Document By ID
    # ==========================================

    @staticmethod
    def get_document(
        document_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Get Document
        # ==========================================

        document = DocumentRepository.get_document(
            document_id,
            db
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        # ==========================================
        # Project-Level READ Access
        # ==========================================

        DocumentService._require_project_access(
            document.project_id,
            current_user,
            db
        )

        return document

    # ==========================================
    # Get Project Documents
    # ==========================================

    @staticmethod
    def get_project_documents(
        project_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Project-Level READ Access
        # ==========================================

        DocumentService._require_project_access(
            project_id,
            current_user,
            db
        )

        # ==========================================
        # Get Documents
        # ==========================================

        return DocumentRepository.get_project_documents(
            project_id,
            db
        )

    # ==========================================
    # Delete Document
    # ==========================================

    @staticmethod
    def delete_document(
        document_id: int,
        current_user: dict,
        db: Session
    ):

        # ==========================================
        # Get Document
        # ==========================================

        document = DocumentRepository.get_document(
            document_id,
            db
        )

        if document is None:

            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        # ==========================================
        # Only Global Admin Can Delete
        # ==========================================

        require_admin(
            current_user
        )

        # ==========================================
        # Activity Log
        # ==========================================

        ActivityRepository.create_activity(
            project_id=document.project_id,
            user_id=current_user["user_id"],
            action="DELETE",
            entity_type="DOCUMENT",
            entity_id=document.id,
            description=(
                f"Deleted document: "
                f"{document.file_name}"
            ),
            db=db
        )

        # ==========================================
        # Delete Document
        # ==========================================

        return DocumentRepository.delete_document(
            document_id,
            db
        )