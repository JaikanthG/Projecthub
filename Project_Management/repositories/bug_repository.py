from sqlalchemy.orm import Session

from ..models import Bug


class BugRepository:

    @staticmethod
    def get_all_bugs(
        db: Session
    ):
        return db.query(Bug).all()

    @staticmethod
    def get_bug_by_id(
        bug_id: int,
        db: Session
    ):
        return (
            db.query(Bug)
            .filter(
                Bug.id == bug_id
            )
            .first()
        )

    @staticmethod
    def get_bug_by_title(
        title: str,
        db: Session
    ):
        return (
            db.query(Bug)
            .filter(
                Bug.title == title
            )
            .first()
        )

    @staticmethod
    def create_bug(
        bug: Bug,
        db: Session
    ):

        db.add(bug)
        db.commit()
        db.refresh(bug)

        return bug

    @staticmethod
    def update_bug(
        db: Session
    ):

        db.commit()

    @staticmethod
    def delete_bug(
        bug: Bug,
        db: Session
    ):

        db.delete(bug)
        db.commit()