from enum import Enum


class AttachSessionClientRequestMode(str, Enum):
    CONTROLLER = "controller"
    OBSERVER = "observer"

    def __str__(self) -> str:
        return str(self.value)
