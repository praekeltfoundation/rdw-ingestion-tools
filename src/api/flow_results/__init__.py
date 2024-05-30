from collections.abc import Iterator

from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("FLOW_RESULTS_API_KEY")
BASE_URL = config_from_env("FLOW_RESULTS_API_BASE_URL")


def get_ids(client: Client, **kwargs: str | int) -> Iterator[str]:
    """Returns a list of flow id's.

    These id's are required in order to get responses from the Flow
    Results API.

    """

    params = {**kwargs}
    url = ""

    response = client.get(url, params=params)
    response.raise_for_status()

    for flow in response.json()["data"]:
        yield flow["id"]


def get_paginated(
    client: Client,
    url: str,
    **kwargs: str | int,
) -> Iterator[list]:
    """Paginate over the Flow Results Responses Endpoint.

    Each response returns a next link which is followed until
    the full result set is returned.

    """

    while True:
        response = client.get(url, params={**kwargs})
        response.raise_for_status()

        data: dict = response.json()

        results: list = data["data"]["attributes"]["responses"]
        yield from results

        try:
            url = data["data"]["relationships"]["links"]["next"].split(
                "packages/"
            )[-1]
        except AttributeError:
            break


headers = {"Authorization": f"Token {API_KEY}"}

client: Client = Client(base_url=BASE_URL, headers=headers)

from .main import pyFlows as pyFlows
