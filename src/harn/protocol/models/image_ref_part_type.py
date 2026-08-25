from enum import Enum


class ImageRefPartType(str, Enum):
    IMAGE_REF = "image_ref"

    def __str__(self) -> str:
        return str(self.value)
