from enum import Enum


class LiveSessionClientMode(str, Enum):
    CONTROLLER = "controller"
    OBSERVER = "observer"

    def __str__(self) -> str:
        return str(self.value)
