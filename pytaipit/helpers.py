"""Helpers and utils."""
from __future__ import annotations

from const import REGIONS, UNKNOWN


def get_region_name(region_id: int) -> str:
    region_name = REGIONS.get(region_id, f'{UNKNOWN} <{region_id}>')
    return region_name
