from sqlalchemy.orm import Session

from ..models import RCAReport


class RCARepository:

    @staticmethod
    def create_rca(
        rca: RCAReport,
        db: Session
    ):

        db.add(rca)
        db.commit()
        db.refresh(rca)

        return rca

    @staticmethod
    def get_all_rcas(
        db: Session
    ):

        return (
            db.query(RCAReport)
            .order_by(
                RCAReport.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_rca_by_id(
        rca_id: int,
        db: Session
    ):

        return (
            db.query(RCAReport)
            .filter(
                RCAReport.id == rca_id
            )
            .first()
        )

    @staticmethod
    def get_rca_by_bug(
        bug_id: int,
        db: Session
    ):

        return (
            db.query(RCAReport)
            .filter(
                RCAReport.bug_id == bug_id
            )
            .first()
        )

    @staticmethod
    def get_project_rcas(
        project_id: int,
        db: Session
    ):

        return (
            db.query(RCAReport)
            .filter(
                RCAReport.project_id == project_id
            )
            .order_by(
                RCAReport.created_at.desc()
            )
            .all()
        )

    @staticmethod
    def update_rca(
        db: Session
    ):

        db.commit()

    @staticmethod
    def delete_rca(
        rca: RCAReport,
        db: Session
    ):

        db.delete(rca)
        db.commit()