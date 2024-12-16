from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("TURN_BQ_API_KEY")
BASE_URL = config_from_env("TURN_BQ_API_BASE_URL")

session_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

client: Client = Client(
    base_url=BASE_URL, headers=session_headers, timeout=30.0
)


from .main import pyTurnBQ as pyTurnBQ
