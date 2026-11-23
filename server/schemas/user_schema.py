from pydantic import BaseModel, Field, ConfigDict

from server.constants import UserRole

### --------------------------------------------------###

class UserBase(BaseModel):
    username: str = Field(min_length = 5, max_length = 50)
    role: UserRole = UserRole.COMMERCIAL

class UserCreate(UserBase):
    password: str = Field(min_length = 6) #Plaintext password from client

class UserResponse(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes = True)

class UserUpdate(BaseModel):
    username: str | None = Field(default = None, min_length = 5, max_length = 50)
    role: UserRole | None = None
    password: str | None = Field(default = None, min_length = 6)
    is_active: bool | None = None
    