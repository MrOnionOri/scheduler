from sqlalchemy import String, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Manager dueño del proyecto (nullable si lo crea Admin y aún no asigna)
    owner_manager_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)

    teams = relationship("Team", back_populates="project", cascade="all, delete-orphan")
