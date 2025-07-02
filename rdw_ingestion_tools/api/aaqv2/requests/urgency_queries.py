from io import StringIO

from attrs import define
from httpx import Client
from polars import LazyFrame, read_json

from ..extensions.httpx import get
from ..schemas.urgency_queries import urgency_queries_schema


@define
class UrgencyQueries:
    """Dedicated to the urgency-queries endpoint of the AAQ V2
    Data Export API.

    """

    client: Client

    def get_urgency_queries(
        self, start_date: str, end_date: str, **kwargs: str | int
    ) -> LazyFrame:
        """Get a Polars LazyFrame of urgency queries.

        This endpoint supports time-based query parameters which can
        be passed to this method as kwargs in the following example:

        pyAAQV2.urgency_queries.get_urgency_queries(
            start_date="2021-01-01T00:00:00"
            end_date="2021-01-02T00:00:00"
            )

        """

        url = "urgency-queries"

        params = {
            "start_date": start_date,
            "end_date": end_date,
            **kwargs,
        }

        urgency_queries_generator = get(self.client, url, **params)

        return read_json(
            StringIO(urgency_queries_generator), schema=urgency_queries_schema
        ).lazy()
