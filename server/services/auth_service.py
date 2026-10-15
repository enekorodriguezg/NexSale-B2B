from sqlalchemy.orm import Session
from sqlalchemy import select

from server.models import User
from server.core.security import verify_password

### --------------------------------------------------###

def login(db: Session, username: str, plain_password: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        return None

    if not verify_password(plain_password = plain_password, salt = user.salt, hashed_password = user.hashed_password): #type: ignore
        return None

    return user

