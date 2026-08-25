from enum import Enum


class PermissionRequestObject(str, Enum):
    PERMISSION_REQUEST = "permission_request"

    def __str__(self) -> str:
        return str(self.value)
