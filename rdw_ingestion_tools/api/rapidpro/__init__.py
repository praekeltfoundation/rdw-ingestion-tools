from collections.abc import Iterator

from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("RAPIDPRO_API_KEY")
BASE_URL = config_from_env("RAPIDPRO_API_BASE_URL")


def get_paginated(
    client: Client,
    url: str,
    **kwargs: str | int,
) -> Iterator[dict]:
    """Paginate over a Rapidpro API endpoint.

    The Rapidpro API returns a next token with each response until no further
    pages are left to return.

    """

    while True:
        response = client.get(url, params={**kwargs})
        response.raise_for_status()

        data: dict = response.json()

        results: list = data["results"]
        yield from results

        try:
            url = data["next"].split("/v2/")[1]
        except AttributeError:
            break


headers = {"Authorization": f"Token {API_KEY}"}

client: Client = Client(base_url=BASE_URL, headers=headers)


from .main import pyRapid as pyRapid
