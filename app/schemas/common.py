from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Generic operational confirmation message response."""
    message: str
