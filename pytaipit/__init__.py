"""Taipit API wrapper."""
from __future__ import annotations

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")

from .api import TaipitApi
from .auth import AbstractTaipitAuth, SimpleTaipitAuth

__all__ = [
    "TaipitApi",
    "AbstractTaipitAuth",
    "SimpleTaipitAuth",
    __version__
]
