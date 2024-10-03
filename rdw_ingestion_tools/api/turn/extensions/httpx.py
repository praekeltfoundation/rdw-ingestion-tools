from collections.abc import Iterator

from httpx import Client


def get_paginated(
    client: Client, url: str, start: str, end: str, **kwargs: str | int
) -> Iterator[dict]:
    """Paginate over Turn Data Export API. [Likely to be deprecated soon.]

    This method will request a cursor from the Turn Data Export API and
    use this to page through the data the API returns.

    """
    url = f"{url}/cursor"

    data = {"from": start, "until": end}

    cursor_response = client.post(url, json=data, params={**kwargs})
    cursor_response.raise_for_status()

    cursor = cursor_response.json()["cursor"]

    while True:
        response = client.get(f"{url}/{cursor}")
        response.raise_for_status()

        response_json: dict = response.json()

        response_data: list[dict] = response_json["data"]
        yield from response_data

        try:
            cursor = response.json["paging"]["next"]
        except TypeError:
            break
