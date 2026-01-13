from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    owner_manager_id: int | None = None  # solo Admin lo debería mandar

class ProjectOut(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    owner_manager_id: int | None

class TeamCreate(BaseModel):
    name: str

class TeamOut(BaseModel):
    id: int
    project_id: int
    name: str
