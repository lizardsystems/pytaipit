import pytest
from requests import Session

from pytaipit import SimpleTaipitAuth, TaipitApi
from .common import (
    TEST_USERNAME,
    TEST_PASSWORD,
    TEST_CLIENT_ID,
    TEST_CLIENT_SECRET
)


@pytest.fixture(scope='class')
def auth() -> SimpleTaipitAuth:
    with Session() as _session:
        _auth = SimpleTaipitAuth(
            username=TEST_USERNAME,
            password=TEST_PASSWORD,
            session=_session,
            client_id=TEST_CLIENT_ID,
            client_secret=TEST_CLIENT_SECRET
        )
        yield _auth
        # some finalization


@pytest.fixture(scope='class')
def api(auth: SimpleTaipitAuth) -> TaipitApi:
    _api = TaipitApi(auth)
    yield _api
    # some finalization
