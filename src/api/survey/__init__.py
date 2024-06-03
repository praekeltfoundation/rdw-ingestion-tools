from collections.abc import Iterator

from httpx import Client

from .. import config_from_env

API_KEY = config_from_env("SURVEY_API_KEY")
BASE_URL = config_from_env("SURVEY_API_BASE_URL")


def get_paginated(
    client: Client, url: str, start: str, max_pages: int, **kwargs: str | int
) -> Iterator[dict]:
    """Paginates over the custom MQR Survey API endpoint."""
    pages = 0

    params = {"updated_at_gt": start, **kwargs}

    while pages < max_pages:
        response = client.get(url=url, params=params)
        response.raise_for_status()

        data: dict = response.json()["results"]
        yield from data

        url = response.json()["next"]

        if not url:
            break

        pages += 1


headers = {"Authorization": f"Token {API_KEY}"}

client: Client = Client(base_url=BASE_URL, headers=headers)

from .main import pySurvey as pySurvey
