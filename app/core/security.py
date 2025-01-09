from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.cache.redis import set_user_token
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(minutes=settings.JWT_EXPIRATION)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.JWT_SECRET,
                       algorithm=settings.ALGORITHM)

    user_id = data["sub"]
    await set_user_token(user_id, token)

    return token
