from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserBase(BaseModel):
    name: str = Field(..., max_length=255, description="Full name or display name of the user.")
    email: EmailStr = Field(..., description="Unique email address of the user.")


class UserLogin(BaseModel):
    """Schema for user authentication request payload."""
    email: EmailStr = Field(..., description="User email address for authentication.")
    password: str = Field(..., min_length=6, max_length=128, description="Plaintext password for verification.")


class UserRegister(BaseModel):
    """Schema for new user registration request payload."""
    name: str = Field(..., min_length=1, max_length=255, description="Full name or display name.")
    email: EmailStr = Field(..., description="Valid email address.")
    password: str = Field(..., min_length=8, max_length=128, description="Strong password for account security.")


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile information."""
    name: str | None = Field(None, min_length=1, max_length=255, description="Updated name.")
    email: EmailStr | None = Field(None, description="Updated email address.")


class UserPasswordUpdate(BaseModel):
    """Schema for changing user password."""
    current_password: str = Field(..., description="Existing plaintext password.")
    password: str = Field(..., min_length=8, max_length=128, description="New strong password.")
    password_confirmation: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Confirmation of the new password.",
    )

    @model_validator(mode="after")
    def validate_passwords_match(self) -> Self:
        if self.password != self.password_confirmation:
            raise ValueError("Passwords do not match")
        return self


class UserResponse(UserBase):
    """Schema for public user profile response (excluding sensitive credentials)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email_verified_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
