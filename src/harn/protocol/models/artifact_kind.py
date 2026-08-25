from enum import Enum


class ArtifactKind(str, Enum):
    DATASET = "dataset"
    DIFF = "diff"
    FILE = "file"
    IMAGE = "image"
    LOG = "log"
    OTHER = "other"
    PATCH = "patch"
    RECEIPT = "receipt"
    SNAPSHOT = "snapshot"

    def __str__(self) -> str:
        return str(self.value)
