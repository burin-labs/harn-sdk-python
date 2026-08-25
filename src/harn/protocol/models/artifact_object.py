from enum import Enum


class ArtifactObject(str, Enum):
    ARTIFACT = "artifact"

    def __str__(self) -> str:
        return str(self.value)
