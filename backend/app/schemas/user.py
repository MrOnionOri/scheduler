from pydantic import BaseModel, EmailStr

class MeOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    roles: list[str]
