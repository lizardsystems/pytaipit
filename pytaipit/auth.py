"""Taipit API Auth wrapper."""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Dict, Any, cast, Optional

from requests import Session

from .const import (
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET,
    DEFAULT_TOKEN_URL,
    DEFAULT_BASE_URL, TOKEN_REQUIRED_FIELDS, LOGGER
)
from .exceptions import (
    TaipitInvalidTokenResponse,
    TaipitAuthInvalidGrant,
    TaipitAuthInvalidClient,
    TaipitAuthError,
    TaipitTokenRefreshFailed,
    TaipitTokenAcquireFailed
)

CLOCK_OUT_OF_SYNC_MAX_SEC = 20


class AbstractTaipitAuth(ABC):
    """Abstract class to make authenticated requests."""
    _session: Session
    _base_url: str

    def __init__(self, session: Session | None = None, base_url: str = DEFAULT_BASE_URL):
        """Initialize the auth."""
        self._session = session if session else Session()
        self._base_url = base_url

    @abstractmethod
    def get_access_token(self) -> str:
        """Return a valid access token."""

    def request(self, method: str, url: str, **kwargs) -> Any:
        """Make a request with token authorization."""
        _url = f"{self._base_url}/{url}"
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        access_token = self.get_access_token()
        kwargs["headers"]["Authorization"] = f"Bearer {access_token}"

        LOGGER.debug("Request to %s with data %s", url, kwargs)

        response = self._session.request(method, _url, **kwargs)
        response.raise_for_status()
        data = response.json()
        LOGGER.debug("Request finished with status=%s, headers=%s, data=%s",
                     response.status_code, response.headers, data)
        return data


class SimpleTaipitAuth(AbstractTaipitAuth):
    """Simple implementation of AbstractFlickAuth that gets a token once."""
    _username: str
    _password: str
    _client_id: str
    _client_secret: str
    _token_url: str
    _token: Optional[Dict[str, Any]] = None

    def __init__(self, username: str, password: str,
                 session: Session | None = None,
                 client_id: str = DEFAULT_CLIENT_ID,
                 client_secret: str = DEFAULT_CLIENT_SECRET,
                 base_url: str = DEFAULT_BASE_URL,
                 token_url: str = DEFAULT_TOKEN_URL):
        super().__init__(session, base_url)
        self._username = username
        self._password = password
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_url = token_url

    def _token_request(self, data: dict) -> dict:
        """Make a token request."""
        _url = f"{self._base_url}/{self._token_url}"
        data["client_id"] = self._client_id
        data["client_secret"] = self._client_secret

        LOGGER.debug("Token request %s with data %s",
                     _url, data)

        response = self._session.get(_url, params=data)

        if response.status_code == 400:
            error_info = response.json()
            if error_info['error'] == 'invalid_grant':
                raise TaipitAuthInvalidGrant(error_info['error_description'])
            if error_info['error'] == 'invalid_client':
                raise TaipitAuthInvalidClient(error_info['error_description'])
            raise TaipitAuthError

        response.raise_for_status()

        new_token = response.json()

        if not self._is_valid_token(new_token):
            raise TaipitInvalidTokenResponse

        new_token["expires_in"] = int(new_token["expires_in"])
        new_token["expires_at"] = time.time() + new_token["expires_in"]

        LOGGER.debug("Token request finished %s", new_token)

        return cast(dict, new_token)

    def _refresh_token(self, token: dict) -> dict:
        """Refresh tokens."""
        try:
            new_token = self._token_request(
                {
                    "grant_type": "refresh_token",
                    "refresh_token": token["refresh_token"],
                }
            )
        except (TaipitAuthInvalidGrant, TaipitAuthInvalidClient):
            raise
        except Exception as exc:
            raise TaipitTokenRefreshFailed from exc

        return cast(dict, new_token)

    def _new_token(self) -> dict:
        """Refresh tokens."""
        try:
            new_token = self._token_request(
                {
                    "grant_type": "password",
                    "username": self._username,
                    "password": self._password
                }
            )

        except (TaipitAuthInvalidGrant, TaipitAuthInvalidClient):
            raise
        except Exception as exc:
            raise TaipitTokenAcquireFailed from exc

        return cast(dict, new_token)

    @staticmethod
    def _is_valid_token(token: dict) -> bool:
        """Check if token is valid and contains all required fields."""
        return TOKEN_REQUIRED_FIELDS <= token.keys()

    @staticmethod
    def _is_expired_token(token: dict) -> bool:
        """Check if token is not expired"""
        return (
                cast(float, token["expires_at"])
                < time.time() + CLOCK_OUT_OF_SYNC_MAX_SEC
        )

    def get_access_token(self):
        """Get access token"""
        if self._token:
            if self._is_expired_token(self._token):
                self._token = self._refresh_token(self._token)
        else:
            self._token = self._new_token()

        return self._token["access_token"]
