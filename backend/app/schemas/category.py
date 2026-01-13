from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    color: str = "#3b82f6"

class CategoryOut(BaseModel):
    id: int
    project_id: int
    name: str
    color: str
    is_active: bool
