"""Taipit API wrapper."""
from __future__ import annotations

from typing import List, Any, Union

from .auth import AbstractTaipitAuth
from .const import DEFAULT_API_URL, SECTIONS_ALL, \
    PARAM_ACTION, PARAM_SECTIONS, GET_ENTRIES, PARAM_ID


class TaipitApi:
    """Class to communicate with the Taipit API."""
    _api_url: str

    def __init__(self, auth: AbstractTaipitAuth, api_url: str = DEFAULT_API_URL):
        """Initialize the API and store the auth."""
        self._auth = auth
        self._api_url = api_url

    def get(self, url: str, **kwargs) -> Union[dict[str, Any], list[dict[str, Any]]]:
        """Make async get request to api endpoint"""
        return self._auth.request("GET", f"{self._api_url}/{url}", **kwargs)

    def get_meters(self) -> list[dict[str, Any]]:
        """Get all meters and short info."""
        _url = 'meter/list-all'
        return self.get(_url)

    def get_meter_readings(self, meter_id: int) -> dict[str, Any]:
        """Get readings for meter."""
        _url = 'bmd/all'
        params = {PARAM_ID: meter_id}
        return self.get(_url, params=params)

    def get_own_meters(self) -> list[dict[str, Any]]:
        """Get meters owned by current user."""
        _url = 'meter/list-owner'
        return self.get(_url)

    def get_meter_info(self, meter_id: int) -> dict[str, Any]:
        """Get info for meter."""
        _url = 'meter/get-id'
        params = {PARAM_ID: meter_id}
        return self.get(_url, params=params)

    def get_current_user(self) -> dict[str, Any]:
        """Get current user info."""
        _url = 'user/getuser'
        return self.get(_url)

    def get_user_info(self, user_id: str) -> dict[str, Any]:
        """Get specified user info."""
        _url = f'user/getuserinfo/{user_id}'
        return self.get(_url)

    def get_warnings(self) -> dict[str, Any]:
        """List warnings."""
        _params = {PARAM_ACTION: GET_ENTRIES}
        _url = f'warnings/list'
        return self.get(_url, params=_params)

    def get_settings(self, sections: List[str] = SECTIONS_ALL) -> dict[str, Any]:
        """Get settings"""
        _params = {PARAM_SECTIONS: ','.join(sections)}
        _url = f'config/settings'
        return self.get(_url, params=_params)
