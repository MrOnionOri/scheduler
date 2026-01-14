from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.team import Team
from app.models.project import Project
from app.models.membership import Membership
from app.schemas.team import AddMemberIn, MembershipOut, SetLeaderIn
from app.services.permissions import can_manage_project, is_pl_of_team, can_access_project
from app.schemas.team import AddMemberIn, MembershipOut, SetLeaderIn, TeamCreateIn, TeamUpdateIn, TeamOut


router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/{team_id}/members", response_model=list[MembershipOut])
def list_members(
    team_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    if not can_access_project(db, user, team.project_id):
        raise HTTPException(status_code=403, detail="No access")

    rows = db.query(Membership).filter(Membership.team_id == team_id).order_by(Membership.id.asc()).all()
    return [MembershipOut(id=m.id, team_id=m.team_id, user_id=m.user_id, team_role=m.team_role) for m in rows]

@router.post("/{team_id}/members", response_model=MembershipOut)
def add_member(
    team_id: int,
    payload: AddMemberIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Admin/Manager del proyecto O PL de ese team
    if not (can_manage_project(db, user, team.project_id) or is_pl_of_team(db, user, team_id)):
        raise HTTPException(status_code=403, detail="Not allowed")

    # valida user existe
    from app.models.user import User as UserModel
    target = db.get(UserModel, payload.user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    # crea membership si no existe
    existing = (
        db.query(Membership)
        .filter(Membership.team_id == team_id, Membership.user_id == payload.user_id)
        .first()
    )
    if existing:
        # si ya existe, solo actualiza team_role si viene
        existing.team_role = payload.team_role
        db.commit()
        db.refresh(existing)
        return MembershipOut(id=existing.id, team_id=existing.team_id, user_id=existing.user_id, team_role=existing.team_role)

    m = Membership(team_id=team_id, user_id=payload.user_id, team_role=payload.team_role)
    db.add(m)
    db.commit()
    db.refresh(m)
    return MembershipOut(id=m.id, team_id=m.team_id, user_id=m.user_id, team_role=m.team_role)

@router.patch("/{team_id}/leader", response_model=dict)
def set_leader(
    team_id: int,
    payload: SetLeaderIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Solo Admin/Manager del proyecto
    if not can_manage_project(db, user, team.project_id):
        raise HTTPException(status_code=403, detail="Only Admin/Project Manager can set leader")

    # asegurar membership y poner PL
    m = (
        db.query(Membership)
        .filter(Membership.team_id == team_id, Membership.user_id == payload.user_id)
        .first()
    )
    if not m:
        m = Membership(team_id=team_id, user_id=payload.user_id, team_role="PL")
        db.add(m)
        db.commit()
        db.refresh(m)
    else:
        m.team_role = "PL"
        db.commit()

    return {"status": "ok", "leader_user_id": payload.user_id}

@router.get("", response_model=list[TeamOut])
def list_teams(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Permiso para ver proyecto
    if not can_access_project(db, user, project_id):
        raise HTTPException(status_code=403, detail="No access")

    rows = db.query(Team).filter(Team.project_id == project_id).order_by(Team.id.asc()).all()
    return [TeamOut(id=t.id, project_id=t.project_id, name=t.name, color_hex=getattr(t, "color_hex", None)) for t in rows]


@router.post("", response_model=TeamOut)
def create_team(
    payload: TeamCreateIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Solo Admin/Manager del proyecto
    if not can_manage_project(db, user, payload.project_id):
        raise HTTPException(status_code=403, detail="Not allowed")

    # valida project existe
    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    t = Team(
        project_id=payload.project_id,
        name=payload.name.strip(),
        color_hex=payload.color_hex
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return TeamOut(id=t.id, project_id=t.project_id, name=t.name, color_hex=t.color_hex)


@router.patch("/{team_id}", response_model=TeamOut)
def update_team(
    team_id: int,
    payload: TeamUpdateIn,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Solo Admin/Manager del proyecto
    if not can_manage_project(db, user, team.project_id):
        raise HTTPException(status_code=403, detail="Not allowed")

    if payload.name is not None:
        team.name = payload.name.strip()
    if payload.color_hex is not None:
        team.color_hex = payload.color_hex

    db.commit()
    db.refresh(team)
    return TeamOut(id=team.id, project_id=team.project_id, name=team.name, color_hex=getattr(team, "color_hex", None))


@router.delete("/{team_id}", response_model=dict)
def delete_team(
    team_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    team = db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    # Solo Admin/Manager del proyecto
    if not can_manage_project(db, user, team.project_id):
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(team)
    db.commit()
    return {"status": "ok"}