from contextlib import ExitStack
from unittest.mock import patch

import pytest

from src import generators, utils
from src.config import DefaultConfig

MARKER_NAME = "freeze_uuids"
FIXTURE_NAME = "freeze_uuids"
MOCK_NAME = "FrozenUUID"


@pytest.fixture(name=FIXTURE_NAME)
def freeze_uuids(request):
    """A fixture for freezing UUIDs.

    Default configuration can be overridden using the marker:

        @pytest.mark.freeze_uuids(**args)

    Args:
        obj_path (str): Dot notated path to the UUID object to be patched. [default: uuid.uuid4]

        version (int): UUID version for the new patched UUID object. [default: 4]

        namespace (str): Only patch modules within this namespace. If not set, all imported modules
            will be patched. [default: None]

        values (List[UUID.str]): List of predefined UUID strings that will be used by some of the
            side effects. [default: ["00000000-0000-0000-0000-000000000000"]]

        seed (int): Number used as seed in the random generator. [default: 42]

        side_effect (str): Side effect used for generating UUID values. [default: auto_increment]

            Allowed values:

            auto_increment: The first value in `values` will be used as a starting value and
                incremented by one on each call.

            cycle: List of `values` will be used and will be cycled after the last value has been
                reached.

            random: A seeded random generator will be used. The seed is set by `seed`.

            values: List of `values` will be used. A `StopIteration` will be raised when the last
                value is reached.
    """
    kwargs = {}

    marker = utils.get_closest_marker(request.node, MARKER_NAME)
    if marker:
        kwargs = marker.kwargs

    config = DefaultConfig(**kwargs)
    if config.side_effect == "auto_increment":
        side_effect = generators.auto_increment_generator(start_uuid=config.get_uuids()[0])
    elif config.side_effect == "random":
        side_effect = generators.random_generator(seed=config.seed, version=config.version)
    elif config.side_effect == "cycle":
        side_effect = generators.cycle_generator(uuids=config.get_uuids())
    elif config.side_effect == "values":
        side_effect = config.get_uuids()
    else:
        raise ValueError(f"Unknown side effect: {config.side_effect}")

    module_name, attribute_name = utils.resolve_obj_path(obj_path=config.obj_path)
    with ExitStack() as stack:
        for module in utils.find_modules(
            module_name=module_name, attribute_name=attribute_name, namespace=config.namespace
        ):
            stack.enter_context(
                patch.object(module, attribute_name, side_effect=side_effect, name=MOCK_NAME)
            )
        yield


def pytest_collection_modifyitems(items):
    """Inject our fixture into any tests with our marker"""
    for item in items:
        if utils.get_closest_marker(item, MARKER_NAME):
            item.fixturenames.insert(0, FIXTURE_NAME)


def pytest_configure(config):
    """Register our marker"""
    config.addinivalue_line(
        "markers", "{name}(...): use {name} to freeze UUIDs".format(name=MARKER_NAME)
    )
