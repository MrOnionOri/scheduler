from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.user_admin import UserMiniOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/search", response_model=list[UserMiniOut])
def search_users(
    q: str = "",
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Por ahora: cualquiera logueado puede buscar (luego lo restringimos si quieres)
    q = q.strip().lower()
    if not q:
        return []

    rows = (
        db.query(User)
        .filter(User.email.like(f"%{q}%"))
        .order_by(User.id.desc())
        .limit(20)
        .all()
    )
    return [UserMiniOut(id=u.id, email=u.email, full_name=u.full_name) for u in rows]
