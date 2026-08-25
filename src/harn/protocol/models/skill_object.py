from enum import Enum


class SkillObject(str, Enum):
    SKILL = "skill"

    def __str__(self) -> str:
        return str(self.value)
