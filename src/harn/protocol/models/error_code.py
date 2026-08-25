from enum import Enum


class ErrorCode(str, Enum):
    CLIENT_CLOSED_REQUEST = "client_closed_request"
    CONFLICT = "conflict"
    CURSOR_EXPIRED = "cursor_expired"
    DEADLINE_EXCEEDED = "deadline_exceeded"
    IDEMPOTENCY_KEY_REUSED = "idempotency_key_reused"
    INTERNAL_ERROR = "internal_error"
    INVALID_REQUEST = "invalid_request"
    INVALID_STATE_TRANSITION = "invalid_state_transition"
    PAYLOAD_TOO_LARGE = "payload_too_large"
    PERMISSION_DENIED = "permission_denied"
    POLICY_VIOLATION = "policy_violation"
    RATE_LIMITED = "rate_limited"
    RESOURCE_LOCKED = "resource_locked"
    RESOURCE_NOT_FOUND = "resource_not_found"
    SERVICE_UNAVAILABLE = "service_unavailable"
    UNAUTHENTICATED = "unauthenticated"
    UNSUPPORTED_PROTOCOL_VERSION = "unsupported_protocol_version"
    UPSTREAM_UNAVAILABLE = "upstream_unavailable"

    def __str__(self) -> str:
        return str(self.value)
