from pydantic import BaseModel, EmailStr

class UserMiniOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
