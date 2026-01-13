from sqlalchemy.orm import Session

from app.db.session import engine, SessionLocal
from app.db.base import Base

# Importar modelos para registrar tablas
from app.models.role import Role
from app.models.user import User
from app.models.feature import FeatureFlag
from app.core.security import hash_password

DEFAULT_ADMIN_EMAIL = "admin@test.com"
DEFAULT_ADMIN_PASSWORD = "Admin123!"  # cámbialo luego


def get_or_create_role(db: Session, name: str) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if role:
        return role
    role = Role(name=name)
    db.add(role)
    db.flush()
    return role


def get_or_create_feature(db: Session, slug: str, name: str, enabled_for_all: bool = False) -> FeatureFlag:
    feat = db.query(FeatureFlag).filter(FeatureFlag.slug == slug).first()
    if feat:
        # actualiza campos por si cambian
        feat.name = name
        feat.enabled = True
        feat.enabled_for_all = enabled_for_all
        return feat
    feat = FeatureFlag(slug=slug, name=name, enabled=True, enabled_for_all=enabled_for_all)
    db.add(feat)
    db.flush()
    return feat


def get_or_create_user(db: Session, email: str, password: str, full_name: str = "Admin") -> User:
    email = email.lower().strip()
    user = db.query(User).filter(User.email == email).first()
    if user:
        # si ya existe, solo asegúrate que esté activo y nombre set
        user.is_active = True
        if not user.full_name:
            user.full_name = full_name
        return user

    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        is_active=True,
    )
    db.add(user)
    db.flush()
    return user


def ensure_user_roles(user: User, roles: list[Role]):
    existing = {r.name for r in user.roles}
    for r in roles:
        if r.name not in existing:
            user.roles.append(r)


def ensure_feature_roles(feature: FeatureFlag, roles: list[Role]):
    existing = {r.name for r in feature.roles}
    for r in roles:
        if r.name not in existing:
            feature.roles.append(r)


def main():
    # crea tablas (MVP). Luego lo pasamos a Alembic.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Roles
        r_admin = get_or_create_role(db, "ADMIN")
        r_manager = get_or_create_role(db, "MANAGER")
        r_pl = get_or_create_role(db, "PROJECT_LEADER")
        r_member = get_or_create_role(db, "MEMBER")
        r_beta = get_or_create_role(db, "BETA_TESTER")

        # Usuario Admin
        admin = get_or_create_user(db, DEFAULT_ADMIN_EMAIL, DEFAULT_ADMIN_PASSWORD, full_name="Admin")
        ensure_user_roles(admin, [r_admin, r_beta])

        # Features beta (ejemplos)
        beta_menu = get_or_create_feature(db, "beta_menu", "Menú beta (UI)")
        ensure_feature_roles(beta_menu, [r_beta])

        # Otro ejemplo opcional
        sched_exp = get_or_create_feature(db, "scheduler_experimental", "Scheduler experimental")
        ensure_feature_roles(sched_exp, [r_beta])

        db.commit()

        print("✅ Seed completado")
        print(f"Admin: {DEFAULT_ADMIN_EMAIL}")
        print(f"Password: {DEFAULT_ADMIN_PASSWORD}")

    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
