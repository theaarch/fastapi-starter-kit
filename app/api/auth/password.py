from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.user import UserPasswordUpdate

router = APIRouter()


@router.put(
    "/user/password",
    response_model=MessageResponse,
    summary="Change user password",
    description="Updates the user's password after verifying the existing credentials.",
)
async def update_password(
    password_data: UserPasswordUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MessageResponse:
    if not verify_password(password_data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password",
        )

    if password_data.password == password_data.current_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    current_user.password = get_password_hash(password_data.password)
    await db.commit()

    return MessageResponse(message="Password updated successfully")
