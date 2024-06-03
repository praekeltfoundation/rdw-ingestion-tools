from collections.abc import Iterator

from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("TURN_API_KEY")
BASE_URL = config_from_env("TURN_API_BASE_URL")


def get_paginated(
    client: Client, url: str, start: str, end: str, **kwargs: str | int
) -> Iterator[dict]:
    """Paginate over Turn Data Export API. [Likely to be deprecated soon.]

    This method will request a cursor from the Turn Data Export API and
    use this to page through the data the API returns.

    """

    data = {"from": start, "until": end}

    cursor_response = client.post(url, json=data, params={**kwargs})
    cursor_response.raise_for_status()

    while True:
        response = client.get(url + f"/{cursor_response}")
        response.raise_for_status()

        response_data: dict = response.json()["data"]
        yield from response_data

        try:
            cursor_response = response.json()["paging"]["next"]
        except AttributeError:
            break


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/vnd.v1+json",
    "Content-Type": "application/json",
}

client: Client = Client(base_url=BASE_URL, headers=headers)


from .main import pyTurn as pyTurn
