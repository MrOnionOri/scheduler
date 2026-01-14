from pydantic import BaseModel, field_validator
from .common import ColorMixin
from typing import Optional
import re


class AddMemberIn(BaseModel):
    user_id: int
    team_role: str = "MEMBER"  # "PL" o "MEMBER"

class MembershipOut(BaseModel):
    id: int
    team_id: int
    user_id: int
    team_role: str

class SetLeaderIn(BaseModel):
    user_id: int


# class TeamCreate(ColorMixin):
#     project_id: int
#     name: str

# class TeamOut(ColorMixin):
#     id: int
#     project_id: int
#     name: str
    
class UserOut(ColorMixin):
    id: int
    email: str
    full_name: str | None = None
    
# app/schemas/team.py

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

class TeamCreateIn(BaseModel):
    project_id: int
    name: str
    color_hex: str | None = None

    @field_validator("color_hex")
    @classmethod
    def validate_hex(cls, v):
        if v is None:
            return v
        if not HEX_RE.match(v):
            raise ValueError("color_hex must be like #RRGGBB")
        return v

class TeamUpdateIn(BaseModel):
    name: str | None = None
    color_hex: str | None = None

    @field_validator("color_hex")
    @classmethod
    def validate_hex(cls, v):
        if v is None:
            return v
        if not HEX_RE.match(v):
            raise ValueError("color_hex must be like #RRGGBB")
        return v

class TeamOut(BaseModel):
    id: int
    project_id: int
    name: str
    color_hex: Optional[str] = None
