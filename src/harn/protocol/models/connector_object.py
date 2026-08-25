from enum import Enum


class ConnectorObject(str, Enum):
    CONNECTOR = "connector"

    def __str__(self) -> str:
        return str(self.value)
