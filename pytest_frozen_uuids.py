import importlib
import itertools
import random
import uuid
from dataclasses import dataclass, field
from distutils.version import LooseVersion
from typing import Iterator, List, Optional
from unittest.mock import patch

import pytest

MARKER_NAME = "freeze_uuids"
FIXTURE_NAME = "freeze_uuids"


@dataclass
class DefaultConfig:
    obj_path: str = "uuid.uuid4"
    version: int = 4
    values: Optional[List[str]] = field(
        default_factory=lambda: ["00000000-0000-0000-0000-000000000000"]
    )
    cycle: bool = True
    random: bool = False
    seed: int = 42

    def get_uuids(self) -> List[uuid.UUID]:
        assert self.values
        return [uuid.UUID(value) for value in self.values]


def _get_closest_marker(node, name):
    """Get our marker, regardless of pytest version"""
    if LooseVersion(pytest.__version__) < LooseVersion("3.6.0"):
        return node.get_marker(name)
    else:
        return node.get_closest_marker(name)


def _get_object(obj_path: str) -> tuple:
    """Load object from dot notated path.

    Example:
        >>> _get_object("uuid.uuid4")
        (<module 'uuid' from '/usr/lib/python3.9/uuid.py'>, 'uuid4')
    """
    name, attribute = obj_path.rsplit(".", 1)
    module = importlib.import_module(name)

    return module, attribute


def _random_generator(seed: int, version: int) -> Iterator:
    random.seed(seed)
    while True:
        yield uuid.UUID(int=random.getrandbits(128), version=version)


def _cycle_generator(uuids: list) -> Iterator:
    return itertools.cycle(uuids)


@pytest.fixture(name=FIXTURE_NAME)
def freeze_uuids(request):
    """A fixture for freezing UUIDs.

    Default configuration can be overridden through the marker:

        @pytest.mark.freeze_uuids(...)

    Parameters:
        obj_path (str): Dot notated path to the UUID object to be patched. [default: uuid.uuid4]

        version (int): UUID version for the new patched UUID object. [default: 4]

        values (List[UUID.str]): List of predefined UUID strings that will be used as a side effect
            in the patched object. [default: ["00000000-0000-0000-0000-000000000000"]]

        cycle (bool): If true, `values` will be cycled after last value has been reached, thus
            making it an infinite generator. [default: True]

        random (bool): If true, a seeded random generator will be used as the side effect for
            generating the UUID values, takes precedence over `cycle`. [default: False]

        seed (int): Number used as seed in the random generator. [default: 42]
    """
    kwargs = {}

    marker = _get_closest_marker(request.node, MARKER_NAME)
    if marker:
        kwargs = marker.kwargs

    config = DefaultConfig(**kwargs)
    if config.random:
        side_effect = _random_generator(seed=config.seed, version=config.version)
    elif config.cycle:
        side_effect = _cycle_generator(uuids=config.get_uuids())
    else:
        side_effect = config.get_uuids()

    module, attribute = _get_object(obj_path=config.obj_path)
    with patch.object(module, attribute, side_effect=side_effect):
        yield


def pytest_collection_modifyitems(items):
    """Inject our fixture into any tests with our marker"""
    for item in items:
        if _get_closest_marker(item, MARKER_NAME):
            item.fixturenames.insert(0, FIXTURE_NAME)


def pytest_configure(config):
    """Register our marker"""
    config.addinivalue_line(
        "markers", "{name}(...): use {name} to freeze UUIDs".format(name=MARKER_NAME)
    )
