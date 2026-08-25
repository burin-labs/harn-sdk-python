from enum import Enum


class PersonaObject(str, Enum):
    PERSONA = "persona"

    def __str__(self) -> str:
        return str(self.value)
