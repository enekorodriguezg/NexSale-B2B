from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from server.models import User
from server.schemas.user_schema import UserCreate, UserUpdate
from server.core.security import generate_salt, generate_hashed_password

### --------------------------------------------------###

def get_user_by_id(user_id: int, db: Session) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()

def get_user_by_username(username: str, db: Session) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.execute(stmt).scalar_one_or_none()

### --------------------------------------------------###

def get_all_users(order_by: str, sort_order: str, db: Session) -> list[User]:
    allowed_columns : list[str] = ["id", "username", "role"]
    if order_by not in allowed_columns:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Invalid column for order"
        )

    sort_column = getattr(User, order_by)
    if sort_order.lower() == "desc":
        sort_criteria = sort_column.desc()
    
    else:
        sort_criteria = sort_column.asc()

    stmt = select(User).order_by(sort_criteria)
    return list(db.scalars(stmt).all())

def create_user(user_in: UserCreate, db: Session) -> User:
    try:
        if get_user_by_username(username = user_in.username, db = db) is not None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = f"User with username {user_in.username} already exists"
            )

        salt = generate_salt()
        hashed_password = generate_hashed_password(plain_password = user_in.password, salt = salt)

        new_user: User = User(
            username = user_in.username,
            role = user_in.role.value,
            hashed_password = hashed_password
        )

        db.add(new_user)

        db.commit()
        db.refresh(new_user)
        return new_user

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred while creating the user"
        ) from e

def delete_user(user_id: int, db: Session, current_user: User) -> None:
    try:
        user = get_user_by_id(user_id = user_id, db = db)
        if not user:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"User with user ID {user_id} not found" 
            )
        if user.id == current_user.id:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "You can not delete your own account"
            )

        if user.orders:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = f"User with ID {user_id} has pendant orders"
            )

        db.delete(user)
        db.commit()

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred while creating the user"
        ) from e


def update_user(user_id: int, user_in: UserUpdate, db: Session, current_user: User) -> User:
    try:
        user = get_user_by_id(user_id = user_id, db = db)
        if not user:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"User with user ID {user_id} not found" 
            )

        if user_in.username is not None and user_in.username != user.username:
            if get_user_by_username(username = user_in.username, db = db):
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = f"User with username {user_in.username} already exists"
                )
            user.username = user_in.username

        if user_in.role is not None:
            if user.id == current_user.id and user.role != user_in.role:
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = "You can not change your own role"
                )
            user.role = user_in.role

        if user_in.is_active is not None:
            if user.id == current_user.id and not user_in.is_active:
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = "You can not deactivate your own account"
                )

        if user_in.password is not None:
            user.salt = generate_salt()
            user.hashed_password = generate_hashed_password(plain_password = user_in.password, salt = user.salt)

        db.commit()
        db.refresh(user)
        return user

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An error occurred while creating the user"
        ) from e