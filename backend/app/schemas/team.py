from pydantic import BaseModel

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
