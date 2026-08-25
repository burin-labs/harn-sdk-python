from enum import Enum


class QuotaScope(str, Enum):
    ORGANIZATION = "organization"
    PERSONA = "persona"
    TENANT = "tenant"
    WORKSPACE = "workspace"

    def __str__(self) -> str:
        return str(self.value)
