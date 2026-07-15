from fastapi import status

ERROR_HTTP_STATUS: dict[str, int] = {
    # Domain errors
    "DOMAIN_ERROR": status.HTTP_400_BAD_REQUEST,
    "INVALID_ENTITY_STATE": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "BUSINESS_RULE_VIOLATION": status.HTTP_409_CONFLICT,
    # Application errors
    "APPLICATION_ERROR": status.HTTP_400_BAD_REQUEST,
    "VALIDATION_ERROR": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EMAIL_TAKEN": status.HTTP_409_CONFLICT,
    # Infrastructure errors
    "INTERNAL_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def get_http_status_for_error_code(code: str) -> int:
    return ERROR_HTTP_STATUS.get(code, status.HTTP_400_BAD_REQUEST)
