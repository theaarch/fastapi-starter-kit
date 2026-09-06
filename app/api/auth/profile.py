from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserProfileUpdate, UserResponse

router = APIRouter()


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Retrieves profile details of the currently authenticated user.",
)
async def get_my_profile(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Updates name or email of the currently authenticated user.",
)
async def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    if profile_data.email is not None and profile_data.email != current_user.email:
        stmt = select(User).where(User.email == profile_data.email, User.id != current_user.id)
        existing_user = (await db.execute(stmt)).scalar_one_or_none()
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken",
            )
        current_user.email = profile_data.email
        current_user.email_verified_at = None

    if profile_data.name is not None:
        current_user.name = profile_data.name

    await db.commit()
    await db.refresh(current_user)
    return current_user
