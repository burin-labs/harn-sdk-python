from enum import Enum


class RememberRuleScope(str, Enum):
    ALWAYS = "always"
    SESSION = "session"
    USER = "user"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
