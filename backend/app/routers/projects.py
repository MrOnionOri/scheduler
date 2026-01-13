from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.team import Team
from app.schemas.project import ProjectCreate, ProjectOut, TeamCreate, TeamOut
from app.services.permissions import is_admin, is_manager, can_access_project, can_manage_project

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    # Admin: todos
    if is_admin(user):
        rows = db.query(Project).order_by(Project.id.desc()).all()
        return [ProjectOut(**r.__dict__) for r in rows]

    # Manager: sus proyectos
    if is_manager(user):
        rows = db.query(Project).filter(Project.owner_manager_id == user.id).order_by(Project.id.desc()).all()
        return [ProjectOut(**r.__dict__) for r in rows]

    # PL/Member: proyectos donde tiene membership
    rows = (
        db.query(Project)
        .join(Team, Team.project_id == Project.id)
        .join("memberships")  # relationship Team.memberships
        .filter_by(user_id=user.id)
        .order_by(Project.id.desc())
        .all()
    )
    # el join string puede ser frágil; si falla, usamos query directa abajo
    if rows:
        return [ProjectOut(**r.__dict__) for r in rows]

    # fallback robusto
    rows2 = (
        db.query(Project)
        .join(Team, Team.project_id == Project.id)
        .join("memberships")
        .filter_by(user_id=user.id)
        .all()
    )
    return [ProjectOut(**r.__dict__) for r in rows2]

@router.post("", response_model=ProjectOut)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not (is_admin(user) or is_manager(user)):
        raise HTTPException(status_code=403, detail="Only Admin/Manager can create projects")

    owner_id = payload.owner_manager_id
    if is_manager(user):
        # Manager solo crea proyectos propios
        owner_id = user.id

    proj = Project(
        name=payload.name.strip(),
        description=payload.description.strip(),
        owner_manager_id=owner_id,
        is_active=True,
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return ProjectOut(**proj.__dict__)

@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not can_access_project(db, user, project_id):
        raise HTTPException(status_code=403, detail="No access to this project")
    proj = db.get(Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectOut(**proj.__dict__)

@router.post("/{project_id}/teams", response_model=TeamOut)
def create_team(
    project_id: int,
    payload: TeamCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not can_manage_project(db, user, project_id):
        raise HTTPException(status_code=403, detail="Only Admin or project Manager can create teams")

    if not db.get(Project, project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    team = Team(project_id=project_id, name=payload.name.strip())
    db.add(team)
    db.commit()
    db.refresh(team)
    return TeamOut(id=team.id, project_id=team.project_id, name=team.name)

@router.get("/{project_id}/teams", response_model=list[TeamOut])
def list_teams(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if not can_access_project(db, user, project_id):
        raise HTTPException(status_code=403, detail="No access to this project")

    rows = db.query(Team).filter(Team.project_id == project_id).order_by(Team.id.asc()).all()
    return [TeamOut(id=t.id, project_id=t.project_id, name=t.name) for t in rows]
