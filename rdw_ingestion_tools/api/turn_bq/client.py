from functools import lru_cache

from httpx import Client
from httpx_retries import RetryTransport

from .. import config_from_env

API_KEY = config_from_env("TURN_BQ_API_KEY")
BASE_URL = config_from_env("TURN_BQ_API_BASE_URL")

session_headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}


def make_client() -> Client:
    return Client(
        base_url=BASE_URL,
        headers=session_headers,
        timeout=30.0,
        transport=RetryTransport(),
    )


@lru_cache(maxsize=1)
def get_client() -> Client:
    return make_client()
