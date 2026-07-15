from __future__ import annotations

import inspect
from dataclasses import fields
from typing import Any

from mediatr import Mediator

from application.common.behaviors.log import LogBehavior
from application.common.context import ApplicationContext
from application.users.commands.create.handler import CreateUserHandler

# Behaviors run in registration order (outermost first).
Mediator.register_behavior(LogBehavior)

# Import handlers so @Mediator.handler decorators register them.
HANDLERS = (CreateUserHandler,)


def create_mediator(context: ApplicationContext, **dependencies: Any) -> Mediator:
    """
    Build a request-scoped mediator with injected dependencies.

    Shared dependencies live on ``ApplicationContext``.
    Handler-specific dependencies are passed as keyword arguments and matched
    to handler ``__init__`` parameter names.
    """

    def handler_class_manager(handler_cls: type, is_behavior: bool = False) -> object:
        kwargs = _resolve_handler_kwargs(handler_cls, context, dependencies)
        return handler_cls(**kwargs)

    return Mediator(handler_class_manager=handler_class_manager)


def _resolve_handler_kwargs(
    handler_cls: type,
    context: ApplicationContext,
    dependencies: dict[str, Any],
) -> dict[str, Any]:
    available = {field.name: getattr(context, field.name) for field in fields(context)}
    available.update(dependencies)

    parameters = inspect.signature(handler_cls.__init__).parameters
    kwargs: dict[str, Any] = {}

    for name, parameter in parameters.items():
        if name == "self":
            continue
        if parameter.kind is inspect.Parameter.VAR_KEYWORD:
            continue
        if name in available:
            kwargs[name] = available[name]
        elif parameter.default is not inspect.Parameter.empty:
            continue
        else:
            raise TypeError(
                f"{handler_cls.__name__} requires {name!r}, but it was not provided "
                f"via ApplicationContext or create_mediator kwargs."
            )

    return kwargs