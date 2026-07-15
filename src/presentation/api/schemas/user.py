from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class CreateUserRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: Annotated[str, StringConstraints(to_lower=True, min_length=3)]
    name: Annotated[str, StringConstraints(min_length=1)]
    password: Annotated[str, StringConstraints(min_length=8)]


class CreateUserResponse(BaseModel):
    id: int
