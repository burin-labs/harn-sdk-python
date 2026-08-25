from enum import Enum


class ArtifactRefPartType(str, Enum):
    ARTIFACT_REF = "artifact_ref"

    def __str__(self) -> str:
        return str(self.value)
