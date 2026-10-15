from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
import jwt
from pydantic import ValidationError

from server.database import get_db
from server.core.config import SECRET_KEY, ALGORITHM
from server.schemas.auth_schema import TokenData
from server.models import User
from server.constants import UserRole

### --------------------------------------------------###

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/login")
db: Session = Depends(get_db)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = jwt.decode(jwt = token, key = SECRET_KEY, algorithms = [ALGORITHM])
        expiration = decoded_token.get("exp")
        username: str | None= decoded_token.get("sub")
        role: str | None = decoded_token.get("role")

        if (not expiration) or (username is None):
            raise credentials_exception

        token_data: TokenData = TokenData(username = username, role = role)

    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception

    stmt = select(User).where(User.username == token_data.username) #type: ignore
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise credentials_exception

    return user


class RoleChecker:

     allowed_roles: list[UserRole]

     def __init__(self, allowed_roles: list[UserRole]):
         self.allowed_roles = allowed_roles

     def __call__(self, current_user: User = Depends(get_current_user)) -> User:
         if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = "Opperation not allowed"
            )
         return current_user
             
    


