#!/usr/bin/env bash
set -e
pip uninstall -y pytest_frozen_uuids
pip install dist/*.whl
python -c "import pytest_frozen_uuids"
