from httpx import Client

from .. import config_from_env

USER = config_from_env("TURN_BQ_API_USER")
PASS = config_from_env("TURN_BQ_API_PASS")
BASE_URL = config_from_env("TURN_BQ_API_BASE_URL")

token_request_headers = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}

token_request_data = {
    "grant_type": "password",
    "username": f"{USER}",
    "password": f"{PASS}",
    "client_id": "",
    "client_secret": "",
}

token_response = Client().post(
    url=f"{BASE_URL}/token",
    headers=token_request_headers,
    data=token_request_data,
)

token_response.raise_for_status()

access_token = token_response.json()["access_token"]

session_headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

client: Client = Client(
    base_url=BASE_URL, headers=session_headers, timeout=10.0
)


from .main import pyTurnBQ as pyTurnBQ
