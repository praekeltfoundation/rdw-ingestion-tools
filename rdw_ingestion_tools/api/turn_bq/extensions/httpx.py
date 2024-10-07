from collections.abc import Iterator

from httpx import Client


def get_paginated(
    client: Client, url: str, page_size: int = 100, **kwargs: str | int
) -> Iterator[dict]:
    """Paginate over Turn BQ API.

    This function will paginate over returned pages from the Turn BQ API.

    """
    url = f"{url}"

    params: dict[str, int] = {"page": 1, "size": page_size}

    while True:
        response = client.get(url, params={**params, **kwargs})
        response.raise_for_status()

        response_json: dict = response.json()

        response_data: list[dict] = response_json["items"]

        yield from response_data

        if response_json["page"] < response_json["pages"]:
            params["page"] += 1
        else:
            break
