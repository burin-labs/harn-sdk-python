from enum import Enum


class TruncateSessionResponseObject(str, Enum):
    SESSION_TRUNCATE_RESULT = "session.truncate_result"

    def __str__(self) -> str:
        return str(self.value)
