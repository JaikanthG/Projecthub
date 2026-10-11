from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
)

from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector

from .database import Base


# ============================================================
# USER
# ============================================================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    full_name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(50),
        nullable=False,
        default="employee"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ============================================================
# PROJECT
# ============================================================

class Project(Base):

    __tablename__ = "projects"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_name = Column(
        String(200),
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        Text,
        nullable=True
    )

    technology_stack = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="active"
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    creator = relationship(
        "User"
    )


# ============================================================
# PROJECT MEMBER
# ============================================================

class ProjectMember(Base):

    __tablename__ = "project_members"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    permission = Column(
        String(50),
        nullable=False,
        default="viewer"
    )

    assigned_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    assigned_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    project = relationship(
        "Project"
    )

    user = relationship(
        "User",
        foreign_keys=[user_id]
    )

    assigned_by_user = relationship(
        "User",
        foreign_keys=[assigned_by]
    )


# ============================================================
# KNOWLEDGE
# ============================================================

class Knowledge(Base):

    __tablename__ = "knowledge"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    tags = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="published"
    )

    version = Column(
        Integer,
        nullable=False,
        default=1
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    project = relationship(
        "Project"
    )

    creator = relationship(
        "User"
    )

    chunks = relationship(
        "KnowledgeChunk",
        back_populates="knowledge",
        cascade="all, delete-orphan"
    )


# ============================================================
# KNOWLEDGE CHUNK
# ============================================================

class KnowledgeChunk(Base):

    __tablename__ = "knowledge_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    knowledge_id = Column(
        Integer,
        ForeignKey(
            "knowledge.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    # --------------------------------------------------------
    # Embedding vector
    #
    # IMPORTANT:
    # 384 must match the embedding model dimension.
    # --------------------------------------------------------

    embedding = Column(
        Vector(384),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    knowledge = relationship(
        "Knowledge",
        back_populates="chunks"
    )

    project = relationship(
        "Project"
    )


# ============================================================
# BUG
# ============================================================

class Bug(Base):

    __tablename__ = "bugs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(50),
        nullable=False,
        default="open"
    )

    priority = Column(
        String(50),
        nullable=False,
        default="medium"
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    project = relationship(
        "Project"
    )

    creator = relationship(
        "User"
    )


# ============================================================
# TASK
# ============================================================

class Task(Base):

    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="todo"
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    project = relationship(
        "Project"
    )


# ============================================================
# DOCUMENT
# ============================================================

class Document(Base):

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=False
    )

    file_type = Column(
        String(100),
        nullable=True
    )

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    project = relationship(
        "Project"
    )


# ============================================================
# RCA REPORT
# ============================================================

class RCAReport(Base):

    __tablename__ = "rca_reports"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    bug_id = Column(
        Integer,
        ForeignKey(
            "bugs.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    root_cause = Column(
        Text,
        nullable=False
    )

    impact = Column(
        Text,
        nullable=True
    )

    corrective_action = Column(
        Text,
        nullable=True
    )

    preventive_action = Column(
        Text,
        nullable=True
    )

    resolution = Column(
        Text,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False,
        default="open"
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    project = relationship(
        "Project"
    )

    bug = relationship(
        "Bug"
    )


# ============================================================
# ACTIVITY LOG
# ============================================================

class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    action = Column(
        String(100),
        nullable=False
    )

    entity_type = Column(
        String(100),
        nullable=False
    )

    entity_id = Column(
        Integer,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    project = relationship(
        "Project"
    )

    user = relationship(
        "User"
    )


# ============================================================
# NOTIFICATION
# ============================================================

class Notification(Base):

    __tablename__ = "notifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )

    project_id = Column(
        Integer,
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=True,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    message = Column(
        Text,
        nullable=False
    )

    notification_type = Column(
        String(100),
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User"
    )

    project = relationship(
        "Project"
    )