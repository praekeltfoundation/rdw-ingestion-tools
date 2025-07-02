from io import StringIO

from attrs import define
from httpx import Client
from polars import LazyFrame, read_json

from ..extensions.httpx import get
from ..schemas.queries import query_extract_schema


@define
class Queries:
    """Dedicated to the queries endpoint of the AAQ V2 Data Export API."""

    client: Client

    def get_queries(
        self, start_date: str, end_date: str, **kwargs: str | int
    ) -> LazyFrame:
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

        return read_json(
            StringIO(queries_generator), schema=query_extract_schema
        ).lazy()
