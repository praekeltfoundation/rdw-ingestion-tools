from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("TURN_API_KEY")
BASE_URL = config_from_env("TURN_API_BASE_URL")


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

client: Client = Client(base_url=BASE_URL, headers=headers)


from .main import pyTurn as pyTurn
