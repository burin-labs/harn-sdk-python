from enum import Enum


class PermissionResponseRequestOutcome(str, Enum):
    APPROVE = "approve"
    APPROVED = "approved"
    DENIED = "denied"
    DENY = "deny"
    REJECTED = "rejected"
    SELECTED = "selected"

    def __str__(self) -> str:
        return str(self.value)
