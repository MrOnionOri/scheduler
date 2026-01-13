from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.team import Team
from app.models.activity import Activity
from app.models.activity_assignment import ActivityAssignment
from app.schemas.activity import ActivityCreate, ActivityOut
from app.services.permissions import (
    can_access_project, can_manage_project, can_manage_team, can_view_team,
    is_admin, is_manager, is_pl_of_team
)
from app.schemas.activity_update import ActivityUpdate
from app.services.permissions import can_manage_team, can_manage_project

router = APIRouter(prefix="/activities", tags=["activities"])

def now_utc() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

def to_out(a: Activity) -> ActivityOut:
    assignees = [x.user_id for x in a.assignments]
    return ActivityOut(
        id=a.id,
        project_id=a.project_id,
        team_id=a.team_id,
        category_id=a.category_id,
        title=a.title,
        description=a.description,
        start_at=a.start_at,
        end_at=a.end_at,
        priority=a.priority,
        status=a.status,
        kind=a.kind,
        approval_status=a.approval_status,
        created_by=a.created_by,
        approved_by=a.approved_by,
        approval_comment=a.approval_comment or "",
        assignee_user_ids=assignees,
    )

@router.get("", response_model=list[ActivityOut])
def list_activities(
    from_iso: datetime,
    to_iso: datetime,
    project_id: int | None = None,
    team_id: int | None = None,
    mine: bool = True,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Base query en rango de fechas
    q = db.query(Activity).filter(
        and_(Activity.start_at < to_iso, Activity.end_at > from_iso)
    )

    # filtros por proyecto/team con permisos
    if project_id is not None:
        if not can_access_project(db, user, project_id):
            raise HTTPException(status_code=403, detail="No access to project")
        q = q.filter(Activity.project_id == project_id)

    if team_id is not None:
        if not can_view_team(db, user, team_id):
            raise HTTPException(status_code=403, detail="No access to team")
        q = q.filter(Activity.team_id == team_id)

    # mine=True por defecto: devuelve lo asignado al usuario + sus extras
    if mine and not (is_admin(user) or is_manager(user)):
        # assigned
        assigned_ids = db.query(ActivityAssignment.activity_id).filter(ActivityAssignment.user_id == user.id).subquery()
        q = q.filter(
            (Activity.id.in_(assigned_ids)) | (Activity.created_by == user.id)
        )

    rows = q.order_by(Activity.start_at.asc()).all()
    return [to_out(a) for a in rows]

@router.post("", response_model=ActivityOut)
def create_activity(
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Validaciones base proyecto/team
    if not db.get(Project, payload.project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    if not can_access_project(db, user, payload.project_id):
        raise HTTPException(status_code=403, detail="No access to project")

    if payload.team_id is not None:
        team = db.get(Team, payload.team_id)
        if not team or team.project_id != payload.project_id:
            raise HTTPException(status_code=400, detail="team_id invalid for this project")

    # Reglas de permisos por kind:
    # TEAM: solo Admin/Manager del proyecto o PL del team
    if payload.kind == "TEAM":
        if payload.team_id is None:
            raise HTTPException(status_code=400, detail="TEAM activity requires team_id")
        if not can_manage_team(db, user, payload.team_id):
            raise HTTPException(status_code=403, detail="Only Admin/Manager/PL can create TEAM activities")

    # PERSONAL_ASSIGNED: Admin/Manager/PL pueden asignar a alguien (normalmente dentro de su team/proyecto)
    if payload.kind == "PERSONAL_ASSIGNED":
        # si trae team_id, debe poder gestionar el team; si no trae team, debe gestionar el proyecto
        if payload.team_id is not None:
            if not can_manage_team(db, user, payload.team_id):
                raise HTTPException(status_code=403, detail="Not allowed to assign in this team")
        else:
            if not can_manage_project(db, user, payload.project_id):
                raise HTTPException(status_code=403, detail="Not allowed to assign in this project")

    # PERSONAL_EXTRA: cualquier miembro puede crear, pero queda PENDING si NO es Admin/Manager/PL
    approval_status = "NONE"
    if payload.kind == "PERSONAL_EXTRA":
        if is_admin(user) or is_manager(user) or (payload.team_id is not None and is_pl_of_team(db, user, payload.team_id)):
            approval_status = "APPROVED"
        else:
            approval_status = "PENDING"

    created = now_utc()
    a = Activity(
        project_id=payload.project_id,
        team_id=payload.team_id,
        category_id=payload.category_id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        start_at=payload.start_at,
        end_at=payload.end_at,
        priority=payload.priority,
        status="SCHEDULED",
        kind=payload.kind,
        approval_status=approval_status,
        created_by=user.id,
        approved_by=(user.id if approval_status == "APPROVED" else None),
        approval_comment="",
        created_at=created,
        updated_at=created,
    )
    db.add(a)
    db.commit()
    db.refresh(a)

    # Asignaciones:
    # - PERSONAL_EXTRA: se asigna a sí mismo
    # - TEAM / PERSONAL_ASSIGNED: se asigna a la lista (si viene). Si no viene, queda sin asignar (válido para TEAM)
    assignees: list[int] = []
    if payload.kind == "PERSONAL_EXTRA":
        assignees = [user.id]
    else:
        assignees = list(dict.fromkeys(payload.assignee_user_ids))  # unique manteniendo orden

    for uid in assignees:
        db.add(ActivityAssignment(activity_id=a.id, user_id=uid))

    db.commit()
    db.refresh(a)
    return to_out(a)




@router.patch("/{activity_id}", response_model=ActivityOut)
def update_activity(
    activity_id: int,
    payload: ActivityUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    a = db.get(Activity, activity_id)
    if not a:
        raise HTTPException(status_code=404, detail="Activity not found")

    # permiso:
    # - si es actividad extra creada por él -> puede editarla mientras esté PENDING o APPROVED (tú decides luego)
    # - si es TEAM/PERSONAL_ASSIGNED -> Admin/Manager/PL
    if a.kind == "PERSONAL_EXTRA" and a.created_by == user.id:
        pass
    else:
        if a.team_id is not None:
            if not can_manage_team(db, user, a.team_id):
                raise HTTPException(status_code=403, detail="Not allowed")
        else:
            if not can_manage_project(db, user, a.project_id):
                raise HTTPException(status_code=403, detail="Not allowed")

    if payload.title is not None:
        a.title = payload.title.strip()
    if payload.description is not None:
        a.description = payload.description.strip()
    if payload.start_at is not None:
        a.start_at = payload.start_at
    if payload.end_at is not None:
        a.end_at = payload.end_at
    if payload.category_id is not None:
        a.category_id = payload.category_id
    if payload.priority is not None:
        a.priority = payload.priority
    if payload.status is not None:
        a.status = payload.status

    a.updated_at = now_utc()
    db.commit()
    db.refresh(a)
    return to_out(a)
