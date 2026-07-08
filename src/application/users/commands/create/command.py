from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class CreateUserCommand(BaseModel):
    """Input for the CreateUser use case."""

    model_config = ConfigDict(frozen=True)

    email: Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True)]
    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    password: Annotated[str, StringConstraints(min_length=8)]
