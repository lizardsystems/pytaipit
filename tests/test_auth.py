import pytest


@pytest.mark.asyncio
class TestTaipitAuth:
    def test_new_token(self, auth):
        token = auth._new_token()
        assert 'access_token' in token
        assert 'expires_in' in token
        assert 'expires_at' in token
        assert 'refresh_token' in token
        assert 'token_type' in token
        assert 'scope' in token
        assert token['scope'] is None
        assert token['token_type'] == 'bearer'
        assert token['expires_in'] == 3600
        auth._token = token

    def test_valid_token(self, auth):
        assert auth._is_valid_token(auth._token) is True

    def test_refresh_token(self, auth):
        token = auth._refresh_token(auth._token)
        assert 'access_token' in token
        assert 'expires_in' in token
        assert 'expires_at' in token
        assert 'refresh_token' in token
        assert 'token_type' in token
        assert 'scope' in token
        assert token['scope'] is None
        assert token['token_type'] == 'bearer'
        assert token['expires_in'] == 3600
        auth._token = token
