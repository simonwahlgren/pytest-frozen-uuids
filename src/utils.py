import sys
from distutils.version import LooseVersion
from typing import Iterator, Optional

import pytest


def get_closest_marker(node, name):
    """Get our marker, regardless of pytest version"""
    if LooseVersion(pytest.__version__) < LooseVersion("3.6.0"):
        return node.get_marker(name)
    else:
        return node.get_closest_marker(name)


def resolve_obj_path(obj_path: str) -> tuple:
    """Resolve object module and attribute names from dot notated path.

    Example:
        >>> _resolve_obj_path("uuid.uuid4")
        ("uuid", "uuid4")
        >>> _resolve_obj_path("foo.bar.baz.uuid4")
        ("foo,bar.baz", "uuid4")
    """
    module_name, attribute_name = obj_path.rsplit(".", 1)

    return module_name, attribute_name


def find_modules(module_name: str, attribute_name: str, namespace: Optional[str]) -> Iterator:
    """Find globally and locally imported modules with an attribute.

    Examples:
        >>> # /app/utils.py:
        >>> import uuid  # global import
        >>> from uuid import uuid4  # local import

        >>> import app
        >>> modules = _find_modules('uuid', 'uuid4)
        >>> print(next(modules))
        >>> print(next(modules))
        <module 'uuid' from '/usr/lib/python3.9/uuid.py'>
        <module 'app.utils' from '/app/utils.py'>
    """
    for _, module in sys.modules.items():
        attribute = getattr(module, attribute_name, None)
        if not attribute:
            continue

        if namespace and namespace not in module.__name__:
            continue

        if attribute.__module__ == module_name:
            yield module
