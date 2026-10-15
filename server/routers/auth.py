from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server.schemas.auth_schema import Token, TokenData
from server.database import get_db
from server.services import auth_service
from server.models import User
from server.core.security import create_access_token

### --------------------------------------------------###

router = APIRouter(prefix = "/auth", tags = ["Auth"])

@router.post("/login", response_model = Token, status_code = status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username: str = form_data.username
    plain_password: str = form_data.password
    user: User = auth_service.login(db = db, username = username, plain_password = plain_password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"}
        )

    payload = {"sub": user.username, "role": user.role}
    access_token = create_access_token(data=payload)

    return {"access_token": access_token, "token_type": "bearer"}

    
    
             