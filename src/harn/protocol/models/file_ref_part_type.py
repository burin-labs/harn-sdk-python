from enum import Enum


class FileRefPartType(str, Enum):
    FILE_REF = "file_ref"

    def __str__(self) -> str:
        return str(self.value)
