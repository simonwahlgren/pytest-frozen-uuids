#!/usr/bin/env bash
set -e
python -m pytest tests/unit --cov --no-cov-on-fail --cov-report term-missing
