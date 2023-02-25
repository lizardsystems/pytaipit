"""Provide a CLI for Taipit."""
from __future__ import annotations

import argparse
import logging
from pprint import pprint

from requests import Session

from ._version import __version__
from .api import TaipitApi
from .auth import SimpleTaipitAuth
from .const import (
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET,
    GUEST_USERNAME,
    GUEST_PASSWORD, LOG_LEVELS
)


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Command line tool for Taipit API")
    parser.add_argument("-u", "--username", help="User name")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("--client_id", required=False,
                        help="OAuth credentials client_id (Optional.)",
                        default=DEFAULT_CLIENT_ID)
    parser.add_argument("--client_secret", required=False,
                        help="OAuth credentials client_secret (Optional.)",
                        default=DEFAULT_CLIENT_SECRET)

    # command

    parser.add_argument('id',
                        nargs="?",
                        help='meter ID, if not specified, '
                             'information about all meters will be shown')

    parser.add_argument('--readings',
                        help='show readings for meter', action="store_true")
    parser.add_argument('--info',
                        help='show information about meter', action="store_true")
    parser.add_argument("--user",
                        nargs="?",
                        dest='user_id',
                        help="show info about user, if user_id not specified, "
                             "information about current user will be shown")

    # warnings
    parser.add_argument("--warnings",
                        help="show warnings from the Taipit",
                        action="store_true")
    # settings
    parser.add_argument("--settings",
                        help="show settings for Taipit API",
                        action="store_true")

    parser.add_argument('-v', '--verbose',
                        action='count', default=0,
                        help="increase verbosity level")
    parser.add_argument("-V", "--version",
                        action="version", version=__version__)

    arguments = parser.parse_args()

    return arguments


def cli() -> None:
    """Run main."""
    args = get_arguments()

    # Setup logging and the log level according to the "-v" option
    logging.basicConfig(level=LOG_LEVELS.get(args.verbose, logging.INFO))

    if not args.username:
        username = input(f"User name (default: {GUEST_USERNAME}):")
        if not username:
            username = GUEST_USERNAME
            password = input(f"Password (default: {GUEST_PASSWORD}):")
            if not password:
                password = GUEST_PASSWORD
        else:
            password = input("Password:")
    else:
        username = args.username
        password = args.password

    with Session() as session:
        auth = SimpleTaipitAuth(username, password, session, args.client_id, args.client_secret)
        api = TaipitApi(auth)

        if args.info:
            if args.id:
                print(f"Info about Meter ID={args.id}:")
                _meter_info = api.get_meter_info(args.id)
                pprint(_meter_info)
            else:
                print("Info about all meters:")
                _meters = api.get_own_meters()
                pprint(_meters)
            return

        if args.user_id:
            print(f"Info about User ID={args.user_id}:")
            _user = api.get_user_info(args.user_id)
            pprint(_user)
        else:
            print("Current User Info:")
            _current_user = api.get_current_user()
            pprint(_current_user)

        if args.settings:
            print("Settings:")
            _settings = api.get_settings()
            pprint(_settings)

        if args.warnings:
            print("Warnings:")
            _warnings = api.get_warnings()
            pprint(_warnings)

        if args.readings:
            if args.id:
                print(f"Readings Meter ID={args.id}:")
                _readings = api.get_meter_readings(args.id)
                pprint(_readings)

        # show all reading in all other cases
        print("Readings:")
        _all_readings = api.get_meters()
        pprint(_all_readings)


if __name__ == "__main__":
    cli()
