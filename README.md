# aioTaipit

A  Python API for [Taipit cloud meters](https://cloud.meters.taipit.ru).

## Installation

Use pip to install the library:

```commandline
pip install aiotaipit
```

## Usage

```python
from pprint import pprint
import requests 

from pytaipit import SimpleTaipitAuth, TaipitApi


async def main(username: str, password: str) -> None:
    """Create the aiohttp session and run the example."""
    with requests.Session() as session:
        auth = SimpleTaipitAuth(username, password, session)
        api = TaipitApi(auth)

        meters = api.get_meters()

        pprint(meters)


if __name__ == "__main__":
    _username = "<YOUR_USER_NAME>"
    _password = "<YOUR_PASSWORD>"
    main(_username, _password)

```
The `SimpleTaipitAuth` client also accept custom client ID and secret (this can be found by sniffing the client).

This will return a price object that looks a little like this:

```python
[{'address': 'Санкт-Петербург, Ворошилова, 2',
  'category': 0,
  'ecometerdata': {'P_aver': 0.21986280758339,
                   'P_averSmall': 0.15261778589793,
                   'P_averSmall_': 109.88480584651,
                   'P_aver_': 158.30122146004,
                   'P_aver_TF1': False,
                   'P_aver_TF2': False,
                   'P_aver_TF31': False,
                   'P_aver_TF32': False,
                   'P_aver_TF33': False,
                   'P_norm': 0.0066666666666667,
                   'currentTS': 1671485359,
                   'ecoStatus': None,
                   'lastReading': {'energy_a': 1004.85,
                                   'energy_t1_a': 794.45,
                                   'energy_t2_a': 210.4,
                                   'energy_t3_a': 0,
                                   'ts_tz': 1671483628,
                                   'value': 0.02},
                   'meterCategory': 0,
                   'time': 1671485359,
                   'timezone': 3,
                   'trend': -48.41641561353,
                   'trendTF1': False,
                   'trendTF2': False},
  'id': 2147485997,
  'isLowDataFreq': False,
  'isOwner': False,
  'isVirtual': 0,
  'metername': 'НЕВА МТ 114 (Wi-Fi) (22001110)',
  'owner': {'peopleNumber': None, 'type': 0, 'typeCode': 'person'},
  'serialNumber': '22001110',
  'usericopath': '/uploads/user/photo/3edba895933a54540fbdb88614f24f480a9eeb68.png',
  'username': 'Компания Тайпит',
  'waterHot': False},
 {'address': 'Санкт-Петербург, Ворошилова, 2',
  'category': 0,
  'ecometerdata': {'P_aver': 0.25422232030182,
                   'P_averSmall': 0.2494024938596,
                   'P_averSmall_': 179.56979557891,
                   'P_aver_': 183.04007061731,
                   'P_aver_TF1': False,
                   'P_aver_TF2': False,
                   'P_aver_TF31': False,
                   'P_aver_TF32': False,
                   'P_aver_TF33': False,
                   'P_norm': 0,
                   'currentTS': 1671485359,
                   'ecoStatus': None,
                   'lastReading': {'energy_a': 11595.62,
                                   'energy_t1_a': 10420.94,
                                   'energy_t2_a': 1174.68,
                                   'energy_t3_a': 0,
                                   'ts_tz': 1671483641,
                                   'value': 0},
                   'meterCategory': 0,
                   'time': 1671485359,
                   'timezone': 3,
                   'trend': -3.4702750384005,
                   'trendTF1': False,
                   'trendTF2': False},
  'id': 2147485996,
  'isLowDataFreq': False,
  'isOwner': False,
  'isVirtual': 0,
  'metername': 'НЕВА МТ 114 (Wi-Fi) (22001114)',
  'owner': {'peopleNumber': None, 'type': 0, 'typeCode': 'person'},
  'serialNumber': '22001114',
  'usericopath': '/uploads/user/photo/3edba895933a54540fbdb88614f24f480a9eeb68.png',
  'username': 'Компания Тайпит',
  'waterHot': False}]
```
