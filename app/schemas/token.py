from pydantic import BaseModel


class Token(BaseModel):
    """Schema representing an access token response."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema representing decoded JWT payload claims."""

    sub: str | None = None
    exp: int | None = None
