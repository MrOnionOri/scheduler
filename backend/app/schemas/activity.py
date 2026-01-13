from pydantic import BaseModel
from datetime import datetime

class ActivityCreate(BaseModel):
    project_id: int
    team_id: int | None = None
    category_id: int | None = None

    title: str
    description: str = ""

    start_at: datetime
    end_at: datetime

    priority: str = "MEDIUM"  # LOW|MEDIUM|HIGH
    kind: str = "TEAM"        # TEAM|PERSONAL_EXTRA|PERSONAL_ASSIGNED

    assignee_user_ids: list[int] = []  # para TEAM o PERSONAL_ASSIGNED

class ActivityOut(BaseModel):
    id: int
    project_id: int
    team_id: int | None
    category_id: int | None

    title: str
    description: str
    start_at: datetime
    end_at: datetime

    priority: str
    status: str
    kind: str
    approval_status: str

    created_by: int
    approved_by: int | None
    approval_comment: str

    assignee_user_ids: list[int]

class ApproveIn(BaseModel):
    comment: str = ""

class RejectIn(BaseModel):
    comment: str = ""
