from pydantic import BaseModel, Field, ConfigDict, EmailStr
from server.constants import UserRole

class UserBase(BaseModel):
    username: str = Field(min_length=5)
    email: EmailStr
    role: UserRole = UserRole.COMMERCIAL
    is_active: bool = True



class UserCreate(UserBase):
    password: str = Field(min_length=6) #Plaintext password from client


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
    