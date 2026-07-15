from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from application.common.exceptions import ApplicationException
from domain.exceptions import DomainException
from presentation.api.error_codes import get_http_status_for_error_code


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApplicationException)
    async def handle_application_exception(
        request: Request,
        exc: ApplicationException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=get_http_status_for_error_code(exc.code),
            content={"detail": str(exc), "code": exc.code},
        )

    @app.exception_handler(DomainException)
    async def handle_domain_exception(
        request: Request,
        exc: DomainException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=get_http_status_for_error_code(exc.code),
            content={"detail": str(exc), "code": exc.code},
        )
