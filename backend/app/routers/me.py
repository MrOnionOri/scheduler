from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.feature import FeatureFlag
from app.schemas.user import MeOut
from app.schemas.feature import FeaturesOut

router = APIRouter(prefix="/me", tags=["me"])

@router.get("", response_model=MeOut)
def me(user: User = Depends(get_current_user)):
    return MeOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        roles=[r.name for r in user.roles],
    )

@router.get("/features", response_model=FeaturesOut)
def my_features(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    role_names = {r.name for r in user.roles}
    # Features habilitadas para todos o para roles del usuario
    feats = (
        db.query(FeatureFlag)
        .filter(FeatureFlag.enabled == True)
        .all()
    )

    enabled = []
    for f in feats:
        if f.enabled_for_all:
            enabled.append(f.slug)
            continue
        f_roles = {r.name for r in f.roles}
        if role_names.intersection(f_roles):
            enabled.append(f.slug)

    # Conveniencia: si tiene BETA_TESTER, opcionalmente puedes activar un “beta menu” global
    # (mejor manejarlo como feature real, pero esto sirve para UI)
    if "BETA_TESTER" in role_names and "beta_menu" not in enabled:
        enabled.append("beta_menu")

    return FeaturesOut(features=sorted(set(enabled)))
