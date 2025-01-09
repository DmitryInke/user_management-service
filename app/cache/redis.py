from redis.asyncio import Redis
import json
from app.core.config import settings

redis = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)


async def get_cached_user(user_id: int):
    user = await redis.get(f"user:{user_id}")
    if user:
        return json.loads(user)
    return None


async def cache_user(user_id: int, user_data: dict):
    await redis.set(f"user:{user_id}", json.dumps(user_data), ex=600)


async def set_user_token(user_id: str, token: str):
    await redis.setex(f"user_token:{user_id}", settings.JWT_EXPIRATION * 60, token)


async def get_user_token(user_id: str) -> str:
    return await redis.get(f"user_token:{user_id}")
