# pytest-frozen-uuids

[![CI](https://github.com/simonwahlgren/pytest-frozen-uuids/actions/workflows/main.yaml/badge.svg)](https://github.com/simonwahlgren/pytest-frozen-uuids/actions/workflows/main.yaml)
[![PyPI version](https://badge.fury.io/py/pytest-frozen-uuids.svg)](https://badge.fury.io/py/pytest-frozen-uuids)

Deterministically frozen UUID's for your tests.

## Features

- Freeze UUID's globally and locally.

## Installation

You can install "pytest-frozen-uuids" via
[pip](https://pypi.python.org/pypi/pip/) from
[PyPI](https://pypi.python.org/pypi):

    $ pip install pytest-frozen-uuids

## Usage

Freeze UUID's by using the `freeze_uuids` fixture:

    def test_freeze_uuids(freeze_uuids):
        import uuid
        assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000000"

Or by using the `freeze_uuids` marker:

    import pytest

    @pytest.mark.freeze_uuids
    def test_freeze_uuids():
        import uuid
        assert str(uuid.uuid4()) == "00000000-0000-0000-0000-000000000000"

## Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/).
You can later check coverage with coverage combine && coverage html. Please try to keep coverage at
least the same before you submit a pull request.

## License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license,
"pytest-frozen-uuids" is free and open source software

## Issues

If you encounter any problems, please [file an
issue](https://github.com/simonwahlgren/pytest-frozen-uuids/issues) along with a detailed
description.

## Credits

This [Pytest](https://github.com/pytest-dev/pytest) plugin was generated with
[Cookiecutter](https://github.com/audreyr/cookiecutter) along with
[@hackebrot](https://github.com/hackebrot)'s
[Cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin) template.
