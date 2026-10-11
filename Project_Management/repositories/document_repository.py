import os

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..models import (
    Document,
    Project
)


class DocumentRepository:

    UPLOAD_FOLDER = "uploads"

    @staticmethod
    def upload_document(
        project_id: int,
        file: UploadFile,
        current_user: dict,
        db: Session
    ):

        project = (
            db.query(Project)
            .filter(
                Project.id == project_id
            )
            .first()
        )

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found."
            )

        os.makedirs(
            DocumentRepository.UPLOAD_FOLDER,
            exist_ok=True
        )

        file_path = os.path.join(
            DocumentRepository.UPLOAD_FOLDER,
            file.filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            buffer.write(
                file.file.read()
            )

        extension = (
            file.filename
            .split(".")[-1]
            .lower()
        )

        document = Document(
            project_id=project_id,
            file_name=file.filename,
            file_path=file_path,
            file_type=extension,
            uploaded_by=current_user["user_id"]
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def get_documents(
        db: Session
    ):

        return db.query(Document).all()

    @staticmethod
    def get_document(
        document_id: int,
        db: Session
    ):

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        return document

    @staticmethod
    def get_project_documents(
        project_id: int,
        db: Session
    ):

        return (
            db.query(Document)
            .filter(
                Document.project_id == project_id
            )
            .all()
        )

    @staticmethod
    def delete_document(
        document_id: int,
        db: Session
    ):

        document = (
            db.query(Document)
            .filter(
                Document.id == document_id
            )
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found."
            )

        if os.path.exists(
            document.file_path
        ):
            os.remove(
                document.file_path
            )

        db.delete(document)
        db.commit()

        return {
            "message": "Document deleted successfully."
        }