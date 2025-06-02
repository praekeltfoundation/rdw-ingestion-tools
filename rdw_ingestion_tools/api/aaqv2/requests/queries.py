from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get


@define
class Queries:
    """Dedicated to the queries endpoint of the AAQ V2 Data Export API."""

    client: Client

    def get_queries(
        self, start_date: str, end_date: str, **kwargs: str | int
    ) -> DataFrame:
        """Get a pandas DataFrame of queries.

        This endpoint supports time-based query parameters which can
        be passed to this method as kwargs in the following example:

        pyAAQV2.queries.get_queries(
            start_date="2021-01-01T00:00:00"
            end_date="2021-01-02T00:00:00"
            )

        """

        url = "queries"

        params = {
            "start_date": start_date,
            "end_date": end_date,
            **kwargs,
        }

        queries_generator = get(self.client, url, **params)

        return DataFrame(queries_generator)
