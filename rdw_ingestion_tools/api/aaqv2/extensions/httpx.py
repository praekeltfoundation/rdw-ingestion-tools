from collections.abc import Iterator

from httpx import Client


def get(
    client: Client,
    url: str,
    **kwargs: str | int,
) -> Iterator[dict]:
    """Get data from an AAQV2 endpoint.

    NOTE: This new API doesn't support pagination like the previous API did :/
    Consider opening a PR to their repo for this?

    """

    response = client.get(url, params={**kwargs})
    response.raise_for_status()

    # Creating Polars frames using JSON input types sometimes throws polars.exceptions.ComputeError
    # if the frame contains a date.
    # This is the only input type I could find that reliably does not throw these errors for Datetime fields
    result = response.text

    return result
