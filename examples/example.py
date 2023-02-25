""" Example showing usage of this library """

from pprint import pprint

import requests

from pytaipit import SimpleTaipitAuth, TaipitApi


def main(username: str, password: str) -> None:
    """Create the aiohttp session and run the example."""
    with requests.Session() as session:
        auth = SimpleTaipitAuth(username, password, session)
        api = TaipitApi(auth)

        meters = api.get_meters()

        pprint(meters)


if __name__ == "__main__":
    _username = "guest@taipit.ru"
    _password = "guest"
    main(_username, _password)
