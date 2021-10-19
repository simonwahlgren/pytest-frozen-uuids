#!/usr/bin/env bash
set -e
pip install -e .
pytest tests/ --cov --no-cov-on-fail --cov-report term-missing
