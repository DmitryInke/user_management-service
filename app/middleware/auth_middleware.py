import logging
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from app.cache.redis import get_user_token
from app.core.config import settings

logger = logging.getLogger(__name__)

PROTECTED_ROUTES = ["/api/profile", "/api/update"]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        try:
            if path in PROTECTED_ROUTES:
                token = request.headers.get("Authorization")
                if not token:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail="Authorization header missing"
                    )

                try:
                    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[
                                         settings.ALGORITHM])
                    user_id = payload.get("sub")
                    if not user_id:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

                    stored_token = await get_user_token(user_id)
                    if not stored_token or stored_token != token:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token is invalid or has been revoked"
                        )

                    request.state.user_id = user_id

                except (IndexError, JWTError) as e:
                    logger.error(f"Token decoding error: {str(e)}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

            response = await call_next(request)
            return response

        except HTTPException as http_exc:
            logger.warning(f"HTTPException: {http_exc.detail}")
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"detail": http_exc.detail}
            )

        except Exception as exc:
            logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"}
            )
