from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class ActivityAssignment(Base):
    __tablename__ = "activity_assignments"
    __table_args__ = (
        UniqueConstraint("activity_id", "user_id", name="uq_activity_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    activity = relationship("Activity", back_populates="assignments")
