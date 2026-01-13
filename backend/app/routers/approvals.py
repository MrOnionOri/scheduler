from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.team import Team
from app.models.activity import Activity
from app.schemas.activity import ActivityOut, ApproveIn, RejectIn
from app.services.permissions import can_manage_team, can_manage_project, can_access_project

router = APIRouter(prefix="/approvals", tags=["approvals"])

def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

def to_out(a: Activity) -> ActivityOut:
    assignees = [x.user_id for x in a.assignments]
    return ActivityOut(
        id=a.id, project_id=a.project_id, team_id=a.team_id, category_id=a.category_id,
        title=a.title, description=a.description,
        start_at=a.start_at, end_at=a.end_at,
        priority=a.priority, status=a.status, kind=a.kind, approval_status=a.approval_status,
        created_by=a.created_by, approved_by=a.approved_by,
        approval_comment=a.approval_comment or "",
        assignee_user_ids=assignees,
    )

@router.get("/pending", response_model=list[ActivityOut])
def list_pending(
    project_id: int | None = None,
    team_id: int | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Activity).filter(Activity.approval_status == "PENDING")

    if team_id is not None:
        if not can_manage_team(db, user, team_id):
            raise HTTPException(status_code=403, detail="Not allowed")
        q = q.filter(Activity.team_id == team_id)

    if project_id is not None:
        if not can_manage_project(db, user, project_id):
            raise HTTPException(status_code=403, detail="Not allowed")
        q = q.filter(Activity.project_id == project_id)

    # si no pasan filtros, solo Admin puede ver global
    if project_id is None and team_id is None:
        # Admin/Manager (sus proyectos) / PL (sus teams) lo veremos luego
        # por ahora pedimos al menos filtro para evitar filtrar todo
        raise HTTPException(status_code=400, detail="Provide project_id or team_id")

    rows = q.order_by(Activity.start_at.asc()).all()
    return [to_out(a) for a in rows]

@router.post("/{activity_id}/approve", response_model=ActivityOut)
def approve(
    activity_id: int,
    payload: ApproveIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    a = db.get(Activity, activity_id)
    if not a:
        raise HTTPException(status_code=404, detail="Activity not found")
    if a.approval_status != "PENDING":
        raise HTTPException(status_code=400, detail="Activity is not pending")

    # Permiso: si tiene team_id => manage team; si no => manage project
    if a.team_id is not None:
        if not can_manage_team(db, user, a.team_id):
            raise HTTPException(status_code=403, detail="Not allowed")
    else:
        if not can_manage_project(db, user, a.project_id):
            raise HTTPException(status_code=403, detail="Not allowed")

    a.approval_status = "APPROVED"
    a.approved_by = user.id
    a.approval_comment = payload.comment.strip()
    a.updated_at = now_utc()
    db.commit()
    db.refresh(a)
    return to_out(a)

@router.post("/{activity_id}/reject", response_model=ActivityOut)
def reject(
    activity_id: int,
    payload: RejectIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    a = db.get(Activity, activity_id)
    if not a:
        raise HTTPException(status_code=404, detail="Activity not found")
    if a.approval_status != "PENDING":
        raise HTTPException(status_code=400, detail="Activity is not pending")

    if a.team_id is not None:
        if not can_manage_team(db, user, a.team_id):
            raise HTTPException(status_code=403, detail="Not allowed")
    else:
        if not can_manage_project(db, user, a.project_id):
            raise HTTPException(status_code=403, detail="Not allowed")

    a.approval_status = "REJECTED"
    a.approved_by = user.id
    a.approval_comment = payload.comment.strip()
    a.updated_at = now_utc()
    db.commit()
    db.refresh(a)
    return to_out(a)
