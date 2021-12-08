import itertools
import random
import uuid
from typing import Iterator, List


def random_generator(seed: int, version: int) -> Iterator:
    random.seed(seed)
    while True:
        yield uuid.UUID(int=random.getrandbits(128), version=version)


def cycle_generator(uuids: List[uuid.UUID]) -> Iterator:
    return itertools.cycle(uuids)


def auto_increment_generator(start_uuid: uuid.UUID) -> Iterator:
    next_uuid = start_uuid
    while True:
        yield next_uuid
        next_uuid = uuid.UUID(int=next_uuid.int + 1)
