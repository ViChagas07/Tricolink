from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, model_validator

_SHORT_CODE_PATTERN = r"^[A-Za-z0-9_-]{3,32}$"


class CreateLinkRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    url: Annotated[str, Field(min_length=1, max_length=2048)]
    alias: Annotated[str | None, Field(default=None, pattern=_SHORT_CODE_PATTERN)] = None
    title: Annotated[str | None, Field(default=None, min_length=1, max_length=120)] = None
    expires_at: AwareDatetime | None = None


class UpdateLinkRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(default=None, max_length=120)] = None
    original_url: Annotated[str | None, Field(default=None, min_length=1, max_length=2048)] = None
    expires_at: AwareDatetime | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def _reject_explicit_nulls(self) -> UpdateLinkRequest:
        fields = self.model_fields_set
        if "original_url" in fields and self.original_url is None:
            raise ValueError("original_url cannot be null")
        if "is_active" in fields and self.is_active is None:
            raise ValueError("is_active cannot be null")
        return self


class LinkResponse(BaseModel):
    code: str
    short_url: str
    original_url: str
    title: str | None
    created_at: datetime
    expires_at: datetime | None
    is_active: bool
    click_count: int


class ListLinksResponse(BaseModel):
    items: list[LinkResponse]
    next_cursor: str | None
