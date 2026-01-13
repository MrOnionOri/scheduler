from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)

    name: Mapped[str] = mapped_column(String(120), index=True)

    project = relationship("Project", back_populates="teams")
    memberships = relationship("Membership", back_populates="team", cascade="all, delete-orphan")
    color_hex: Mapped[str | None] = mapped_column(String(7), nullable=True)
