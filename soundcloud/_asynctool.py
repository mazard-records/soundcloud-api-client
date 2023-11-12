from typing import Iterable, TypeVar

IterableItem = TypeVar("IterableItem")


async def aiter(iterable: Iterable[IterableItem]):
    for i in iterable:
        yield i
