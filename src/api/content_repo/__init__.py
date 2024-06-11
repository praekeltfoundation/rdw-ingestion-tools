from collections.abc import Iterator

from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("CONTENT_REPO_API_KEY")
BASE_URL = config_from_env("CONTENT_REPO_BASE_URL")


def get_paginated(
    client: Client, url: str, max_pages: int, **kwargs: str | int
) -> Iterator[dict]:
    """Paginate over a Content Repo API endpoint."""
    pages = 0

    while url and pages < max_pages:
        response = client.get(url, follow_redirects=True, params={**kwargs})
        response.raise_for_status()

        data: dict = response.json()

        results: dict = data["results"]
        yield from results

        url = data["next"]

        pages += 1


headers = {"Authorization": f"Token {API_KEY}"}

client: Client = Client(base_url=BASE_URL, headers=headers)


from .main import pyContent as pyContent
