from __future__ import annotations

from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: Annotated[str, StringConstraints(to_lower=True, min_length=3)]
    name: Annotated[str, StringConstraints(min_length=1)]
    password: Annotated[str, StringConstraints(min_length=8)]


class CreateUserResponse(BaseModel):
    id: int


class UserSummaryResponse(BaseModel):
    """Summary fields returned in user list pages."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime | None
