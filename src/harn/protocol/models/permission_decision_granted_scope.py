from enum import Enum


class PermissionDecisionGrantedScope(str, Enum):
    ALWAYS = "always"
    SESSION = "session"
    USER = "user"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
