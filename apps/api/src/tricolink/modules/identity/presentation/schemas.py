from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: Annotated[str, Field(min_length=1, max_length=254)]
    password: Annotated[str, Field(min_length=1, max_length=128)]


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: Annotated[str, Field(min_length=1, max_length=254)]
    password: Annotated[str, Field(min_length=1, max_length=128)]


class UpdateMeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    display_name: Annotated[str | None, Field(default=None, max_length=80)] = None
    locale: Annotated[str | None, Field(default=None, max_length=8)] = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    display_name: str | None
    locale: str | None
    is_active: bool
    created_at: datetime


class AuthResponse(BaseModel):
    user: UserResponse


class RegisterResponse(BaseModel):
    status: Literal["registered"] = "registered"


class CsrfResponse(BaseModel):
    csrf_token: str
