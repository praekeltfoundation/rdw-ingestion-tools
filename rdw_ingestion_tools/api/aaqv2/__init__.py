from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("AAQV2_API_KEY")
BASE_URL = config_from_env("AAQV2_API_BASE_URL")


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json",
}


client: Client = Client(base_url=BASE_URL, headers=headers)

from .main import pyAAQV2 as pyAAQV2
