from enum import Enum


class VaultObject(str, Enum):
    VAULT = "vault"

    def __str__(self) -> str:
        return str(self.value)
