from pydantic import BaseModel

class CategoryCount(BaseModel):
    category_id: int | None
    category_name: str
    count: int

class CategoryBarOut(BaseModel):
    project_id: int
    from_iso: str
    to_iso: str
    data: list[CategoryCount]
