from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def choices(cls):
        return [(member.value, member.value) for member in cls]
