#!/usr/bin/env bash
set -e
pytest tests/ --cov --no-cov-on-fail --cov-report term-missing
