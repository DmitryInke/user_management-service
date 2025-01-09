from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud.user import get_user_by_email, get_user_by_id, save_user
from app.core.security import hash_password
from app.cache.redis import get_cached_user, cache_user
from app.db.schemas import UserCreate, UserUpdate, UserResponse
from app.db.models import User


def build_user_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )


async def create_new_user(db: Session, user_data: UserCreate) -> UserResponse:
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        hashed_password=hashed_pwd,
    )

    save_user(db, new_user)
    return build_user_response(new_user)


async def get_user_profile(db: Session, user_id: int) -> UserResponse:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        cached_user = await get_cached_user(user_id)
        if cached_user:
            return cached_user
    except Exception as e:
        print(f"Failed to retrieve user from cache: {e}")

    user_response = build_user_response(user)
    try:
        await cache_user(user_id, user_response.dict())
    except Exception as e:
        print(f"Failed to cache user: {e}")

    return user_response


async def update_user_profile(
    db: Session, user_id: int, user_update: UserUpdate
) -> UserResponse:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.first_name = user_update.first_name
    user.last_name = user_update.last_name

    save_user(db, user)

    user_response = build_user_response(user)
    try:
        await cache_user(user.id, user_response.dict())
    except Exception as e:
        print(f"Failed to cache updated user: {e}")

    return user_response
