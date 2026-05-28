from collections.abc import Iterator

from httpx import Client


def get(client: Client, url: str, field: str | None = None) -> Iterator[dict]:
    """Get data from a Maxim repositories endpoint."""

    response = client.get(url)
    response.raise_for_status()

    yield from response.json()["data"]


def post(
    client: Client,
    url: str,
    data: dict,
) -> Iterator[dict]:
    """Get data from a Maxim log repositories endpoint."""

    # Page numbers start at 0 while total_pages contains the total number of pages
    total_pages = 1

    while data["page"] < total_pages:
        response = client.post(url, json=data)
        response.raise_for_status()

        yield from response.json()["data"]["logs"]

        # Handle pagination
        data["page"] += 1
        total_pages = response.json()["pagination"]["total"]
