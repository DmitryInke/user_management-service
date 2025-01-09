from fastapi import APIRouter, Depends, Request, HTTPException, Body
from sqlalchemy.orm import Session
from app.db.init_db import get_db
from app.db.schemas import UserResponse, UserUpdate
from app.services.user_service import (
    get_user_profile,
    update_user_profile,
)

router = APIRouter(tags=["User"])


@router.get("/profile", response_model=UserResponse, summary="Retrieve user profile")
async def get_profile(request: Request, db: Session = Depends(get_db)):
    user_id = request.state.user_id
    try:
        user_response = await get_user_profile(db, user_id)
        return user_response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while retrieving the profile: {str(e)}"
        )


@router.put("/update", response_model=UserResponse, summary="Update user profile")
async def update_profile(
    request: Request,
    user_update: UserUpdate = Body(...),
    db: Session = Depends(get_db),
):
    user_id = request.state.user_id
    try:
        updated_user = await update_user_profile(db, user_id, user_update)
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while updating the profile: {str(e)}"
        )
