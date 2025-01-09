from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.db.schemas import UserCreate, UserLogin
from app.services.user_service import create_new_user
from app.services.auth_service import authenticate_user

router = APIRouter(tags=["Authentication"])


@router.post("/register", summary="Register a new user")
async def register(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    try:
        new_user = await create_new_user(db, user)
        return {
            "id": new_user.id,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )


@router.post("/login", summary="Login and retrieve an access token")
async def login(user: UserLogin = Body(...), db: Session = Depends(get_db)):
    try:
        token = await authenticate_user(db, user)
        return token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
