#!/usr/bin/env bash
set -e
twine upload --repository testpypi dist/*
