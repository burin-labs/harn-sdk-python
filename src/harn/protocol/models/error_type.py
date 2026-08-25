from enum import Enum


class ErrorType(str, Enum):
    AUTH_ERROR = "auth_error"
    CONFLICT_ERROR = "conflict_error"
    NOT_FOUND_ERROR = "not_found_error"
    PERMISSION_ERROR = "permission_error"
    RATE_LIMIT_ERROR = "rate_limit_error"
    REQUEST_ERROR = "request_error"
    RUNTIME_ERROR = "runtime_error"
    SERVER_ERROR = "server_error"
    UPSTREAM_ERROR = "upstream_error"

    def __str__(self) -> str:
        return str(self.value)
