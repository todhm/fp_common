from typing import TypedDict, Literal


class EightPercentLinkDict(TypedDict):
    id: int
    index: int
    title: str
    length: int
    state: Literal["P", "R"]
    earningRate: float


class EightPercentProductDict(TypedDict):
    pass