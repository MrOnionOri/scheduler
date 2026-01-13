from sqlalchemy.orm import Session
from app.models.user import User
from app.models.project import Project
from app.models.team import Team
from app.models.membership import Membership
from app.models.user import User
from app.models.project import Project
from app.models.team import Team
from app.models.membership import Membership

def role_names(user: User) -> set[str]:
    return {r.name for r in user.roles}

def is_admin(user: User) -> bool:
    return "ADMIN" in role_names(user)

def is_manager(user: User) -> bool:
    return "MANAGER" in role_names(user)

def can_access_project(db: Session, user: User, project_id: int) -> bool:
    if is_admin(user):
        return True

    proj = db.get(Project, project_id)
    if not proj:
        return False

    if is_manager(user) and proj.owner_manager_id == user.id:
        return True

    # PL/Member: pertenece a algún team del proyecto
    q = (
        db.query(Membership.id)
        .join(Team, Team.id == Membership.team_id)
        .filter(Team.project_id == project_id, Membership.user_id == user.id)
        .first()
    )
    return q is not None

def can_manage_project(db: Session, user: User, project_id: int) -> bool:
    if is_admin(user):
        return True
    proj = db.get(Project, project_id)
    return bool(proj and is_manager(user) and proj.owner_manager_id == user.id)

def is_pl_of_team(db: Session, user: User, team_id: int) -> bool:
    m = (
        db.query(Membership)
        .filter(Membership.team_id == team_id, Membership.user_id == user.id)
        .first()
    )
    return bool(m and m.team_role == "PL")




def role_names(user: User) -> set[str]:
    return {r.name for r in user.roles}

def is_admin(user: User) -> bool:
    return "ADMIN" in role_names(user)

def is_manager(user: User) -> bool:
    return "MANAGER" in role_names(user)

def can_access_project(db: Session, user: User, project_id: int) -> bool:
    if is_admin(user):
        return True

    proj = db.get(Project, project_id)
    if not proj:
        return False

    if is_manager(user) and proj.owner_manager_id == user.id:
        return True

    q = (
        db.query(Membership.id)
        .join(Team, Team.id == Membership.team_id)
        .filter(Team.project_id == project_id, Membership.user_id == user.id)
        .first()
    )
    return q is not None

def can_manage_project(db: Session, user: User, project_id: int) -> bool:
    if is_admin(user):
        return True
    proj = db.get(Project, project_id)
    return bool(proj and is_manager(user) and proj.owner_manager_id == user.id)

def is_member_of_team(db: Session, user: User, team_id: int) -> bool:
    m = db.query(Membership).filter(Membership.team_id == team_id, Membership.user_id == user.id).first()
    return m is not None

def is_pl_of_team(db: Session, user: User, team_id: int) -> bool:
    m = db.query(Membership).filter(Membership.team_id == team_id, Membership.user_id == user.id).first()
    return bool(m and m.team_role == "PL")

def can_manage_team(db: Session, user: User, team_id: int) -> bool:
    team = db.get(Team, team_id)
    if not team:
        return False
    if is_admin(user):
        return True
    if can_manage_project(db, user, team.project_id):
        return True
    if is_pl_of_team(db, user, team_id):
        return True
    return False

def can_view_team(db: Session, user: User, team_id: int) -> bool:
    team = db.get(Team, team_id)
    if not team:
        return False
    if can_access_project(db, user, team.project_id):
        return True
    return is_member_of_team(db, user, team_id)