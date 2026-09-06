from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserLogin

router = APIRouter()


@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user and issue API access token",
    description="Authenticates user credentials and issues a time-bound JWT bearer access token.",
)
async def login(
    login_data: UserLogin,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> Token:
    stmt = select(User).where(User.email == login_data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=user.id,
        extra_claims={
            "name": user.name,
            "email": user.email,
        },
    )

    return Token(access_token=access_token, token_type="bearer")
