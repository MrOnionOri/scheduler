from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.activity import Activity
from app.models.category import Category
from app.schemas.analytics import CategoryBarOut, CategoryCount
from app.services.permissions import can_access_project

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/category_bar", response_model=CategoryBarOut)
def category_bar(
    project_id: int,
    from_iso: datetime,
    to_iso: datetime,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not can_access_project(db, user, project_id):
        raise HTTPException(status_code=403, detail="No access")

    # cuenta actividades por categoría (incluye category_id NULL como "Uncategorized")
    rows = (
        db.query(
            Activity.category_id,
            func.count(Activity.id).label("cnt")
        )
        .filter(Activity.project_id == project_id)
        .filter(Activity.start_at < to_iso, Activity.end_at > from_iso)
        .group_by(Activity.category_id)
        .all()
    )

    # map de nombres
    cat_ids = [r[0] for r in rows if r[0] is not None]
    cats = db.query(Category).filter(Category.id.in_(cat_ids)).all() if cat_ids else []
    name_map = {c.id: c.name for c in cats}

    data = []
    for cat_id, cnt in rows:
        data.append(CategoryCount(
            category_id=cat_id,
            category_name=name_map.get(cat_id, "Uncategorized") if cat_id else "Uncategorized",
            count=int(cnt),
        ))

    return CategoryBarOut(
        project_id=project_id,
        from_iso=from_iso.isoformat(),
        to_iso=to_iso.isoformat(),
        data=data,
    )
