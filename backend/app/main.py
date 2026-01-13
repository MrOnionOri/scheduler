from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base

# Importa modelos para registrar tablas
from app.models.role import Role
from app.models.user import User
from app.models.feature import FeatureFlag
from app.models.project import Project
from app.models.team import Team
from app.models.membership import Membership

from app.routers.auth import router as auth_router
from app.routers.me import router as me_router
from app.routers.projects import router as projects_router
from app.routers.teams import router as teams_router
from app.routers.users import router as users_router

from app.models.category import Category
from app.models.activity import Activity
from app.models.activity_assignment import ActivityAssignment

# routers nuevos
from app.routers.categories import router as categories_router
from app.routers.activities import router as activities_router
from app.routers.approvals import router as approvals_router
from app.routers.analytics import router as analytics_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(auth_router)
    app.include_router(me_router)
    app.include_router(projects_router)
    app.include_router(teams_router)
    app.include_router(users_router)
    app.include_router(categories_router)
    app.include_router(activities_router)
    app.include_router(approvals_router)
    app.include_router(analytics_router)
    return app

app = create_app()
