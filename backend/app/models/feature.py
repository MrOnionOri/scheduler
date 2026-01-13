from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

feature_roles = Table(
    "feature_roles",
    Base.metadata,
    Column("feature_id", ForeignKey("features.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)

class FeatureFlag(Base):
    __tablename__ = "features"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    enabled_for_all: Mapped[bool] = mapped_column(Boolean, default=False)

    roles = relationship("Role", secondary=feature_roles, lazy="joined")
