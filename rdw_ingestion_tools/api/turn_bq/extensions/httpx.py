from collections.abc import Iterator

from httpx import Client

from rdw_ingestion_tools.api.turn_bq import get_client as default_client_factory


def get_paginated(
    client: Client, url: str, page_size: int = 1000, **kwargs: str | int
) -> Iterator[dict]:
    """Paginate over Turn BQ API.

    This function will paginate over returned pages from the Turn BQ API.

    """
    client = client or default_client_factory()
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
