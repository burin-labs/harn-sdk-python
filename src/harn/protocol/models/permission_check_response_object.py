from enum import Enum


class PermissionCheckResponseObject(str, Enum):
    PERMISSION_DECISION = "permission_decision"

    def __str__(self) -> str:
        return str(self.value)
