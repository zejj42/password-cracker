from typing import TypedDict, Union, Literal


class CrackSuccess(TypedDict):
    found: Literal[True]
    range_start: int
    range_end: int
    phone_number: str


class CrackFailure(TypedDict):
    found: Literal[False]


CrackResult = Union[CrackSuccess, CrackFailure]


class ChunkPayload(TypedDict):
    hash: str
    range_start: int
    range_end: int
