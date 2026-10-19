from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get


@define
class Repositories:
    """Dedicated to the repositories endpoint of the Maxim logs API."""

    client: Client

    def get_repositories(self) -> LazyFrame:
        """Get a polars LazyFrame of repositories.

        No time-based query parameters are supported for this endpoint.
        Should return the full contents object or an empty DataFrame if
        no records are returned by the API.

        """

        url = "log-repositories"

        repositories_generator = get(self.client, url)

        return LazyFrame(repositories_generator)
