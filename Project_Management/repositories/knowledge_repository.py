from sqlalchemy.orm import Session

from ..models import Knowledge


class KnowledgeRepository:

    @staticmethod
    def get_all_knowledge(
        db: Session
    ):
        return db.query(Knowledge).all()

    @staticmethod
    def get_knowledge_by_id(
        knowledge_id: int,
        db: Session
    ):
        return (
            db.query(Knowledge)
            .filter(
                Knowledge.id == knowledge_id
            )
            .first()
        )

    @staticmethod
    def get_knowledge_by_title(
        title: str,
        db: Session
    ):
        return (
            db.query(Knowledge)
            .filter(
                Knowledge.title == title
            )
            .first()
        )

    @staticmethod
    def create_knowledge(
        knowledge: Knowledge,
        db: Session
    ):

        db.add(knowledge)
        db.commit()
        db.refresh(knowledge)

        return knowledge

    @staticmethod
    def update_knowledge(
        db: Session
    ):

        db.commit()

    @staticmethod
    def delete_knowledge(
        knowledge: Knowledge,
        db: Session
    ):

        db.delete(knowledge)
        db.commit()