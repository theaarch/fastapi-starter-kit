from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.models.user import User
from app.schemas.common import MessageResponse

router = APIRouter()


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Log out user",
    description="Terminates user session. Client should discard the stored access token.",
)
async def logout(
    current_user: Annotated[User, Depends(get_current_user)],
) -> MessageResponse:
    # Note: For stateless JWTs, the client must discard the token.
    # TODO(security): Integrate a Redis-backed token revocation list for immediate server-side invalidation if needed.
    return MessageResponse(message="Successfully logged out")
