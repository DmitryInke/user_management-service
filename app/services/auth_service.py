from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email
from app.core.security import verify_password, create_access_token
from app.db.schemas import UserLogin


async def authenticate_user(db: Session, user_data: UserLogin) -> str:
    user = get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = await create_access_token(data={"sub": str(user.id)})
    return token
