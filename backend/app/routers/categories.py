from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.services.permissions import can_manage_project, can_access_project

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("", response_model=list[CategoryOut])
def list_categories(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not can_access_project(db, user, project_id):
        raise HTTPException(status_code=403, detail="No access")
    rows = db.query(Category).filter(Category.project_id == project_id, Category.is_active == True).order_by(Category.id.asc()).all()
    return [CategoryOut(id=c.id, project_id=c.project_id, name=c.name, color=c.color, is_active=c.is_active) for c in rows]

@router.post("", response_model=CategoryOut)
def create_category(
    project_id: int,
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not can_manage_project(db, user, project_id):
        raise HTTPException(status_code=403, detail="Only Admin/Project Manager can create categories")

    c = Category(project_id=project_id, name=payload.name.strip(), color=payload.color.strip(), is_active=True)
    db.add(c)
    db.commit()
    db.refresh(c)
    return CategoryOut(id=c.id, project_id=c.project_id, name=c.name, color=c.color, is_active=c.is_active)
