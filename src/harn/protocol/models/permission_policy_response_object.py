from enum import Enum


class PermissionPolicyResponseObject(str, Enum):
    PERMISSION_POLICY = "permission_policy"

    def __str__(self) -> str:
        return str(self.value)
