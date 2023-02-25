"""Exceptions for Taipit."""
from __future__ import annotations


class TaipitError(Exception):
    """Base class for aiotaipit errors."""


class TaipitAuthError(TaipitError):
    """Base class for aiotaipit errors."""


class TaipitAuthInvalidGrant(TaipitAuthError):
    """Invalid username and password combination"""


class TaipitAuthInvalidClient(TaipitAuthError):
    """The client credentials are invalid"""


class TaipitTokenError(TaipitAuthError):
    """Taipit token error"""


class TaipitInvalidTokenResponse(TaipitTokenError):
    """Invalid token response"""


class TaipitTokenAcquireFailed(TaipitTokenError):
    """Taipit token error"""


class TaipitTokenRefreshFailed(TaipitTokenError):
    """Token refresh failed"""
