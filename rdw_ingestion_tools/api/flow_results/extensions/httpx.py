from collections.abc import Iterator

from httpx import Client
from httpx_retries import RetryTransport


def get_ids(client: Client, **kwargs: str | int) -> Iterator[str]:
    """Returns a list of flow id's.

    These id's are required in order to get responses from the Flow
    Results API.

    """

    params = {**kwargs}
    url = ""

    with Client(transport=RetryTransport()) as client:
        response = client.get(url, params=params)
        response.raise_for_status()

        for flow in response.json()["data"]:
            yield flow["id"]


def get_paginated(client: Client, url: str, **kwargs: str | int) -> Iterator[list]:
    """Paginate over the Flow Results Responses Endpoint.

    Each response returns a next link which is followed until
    the full result set is returned.

    """

    while True:
        with Client(transport=RetryTransport()) as client:
            response = client.get(url, params={**kwargs})
            response.raise_for_status()

            data: dict = response.json()["data"]

            results: list = data["attributes"]["responses"]
            yield from results

            try:
                full_url = data["relationships"]["links"]["next"]
                url = full_url.split("packages/")[-1]
            except AttributeError:
                break
