from sqlalchemy import String, Text, ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), nullable=True, index=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(160), index=True)
    description: Mapped[str] = mapped_column(Text, default="")

    start_at: Mapped[DateTime] = mapped_column(DateTime, index=True)
    end_at: Mapped[DateTime] = mapped_column(DateTime, index=True)

    priority: Mapped[str] = mapped_column(String(10), default="MEDIUM")  # LOW|MEDIUM|HIGH
    status: Mapped[str] = mapped_column(String(20), default="SCHEDULED")  # SCHEDULED|IN_PROGRESS|DONE|CANCELLED

    kind: Mapped[str] = mapped_column(String(30), default="TEAM")  # TEAM|PERSONAL_EXTRA|PERSONAL_ASSIGNED
    approval_status: Mapped[str] = mapped_column(String(20), default="NONE")  # NONE|PENDING|APPROVED|REJECTED

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    approved_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    approval_comment: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[DateTime] = mapped_column(DateTime)
    updated_at: Mapped[DateTime] = mapped_column(DateTime)

    assignments = relationship("ActivityAssignment", back_populates="activity", cascade="all, delete-orphan")
