from pydantic import BaseModel, Field

### --------------------------------------------------###

class TokenData(BaseModel):
    sub: str | None = None #sub = Subject
    role: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"