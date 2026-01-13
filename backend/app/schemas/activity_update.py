from pydantic import BaseModel
from datetime import datetime

class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    category_id: int | None = None
    priority: str | None = None
    status: str | None = None
