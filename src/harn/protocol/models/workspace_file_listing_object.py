from enum import Enum


class WorkspaceFileListingObject(str, Enum):
    FILE_LISTING = "file_listing"

    def __str__(self) -> str:
        return str(self.value)
