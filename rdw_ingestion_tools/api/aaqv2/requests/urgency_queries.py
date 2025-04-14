from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get


@define
class UrgencyQueries:
    """Dedicated to the urgency-queries endpoint of the AAQ V2
    Data Export API.

    """

    client: Client

    def get_urgency_queries(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of urgency queries.

        This endpoint supports time-based query parameters which can
        be passed to this method as kwargs in the following example:

        pyAAQV2.urgency_queries.get_urgency_queries(
            start_date="2021-01-01T00:00:00"
            end_date="2021-01-02T00:00:00"
            )

        """

        url = "urgency-queries"

        urgency_queries_generator = get(self.client, url, **kwargs)

        return DataFrame(urgency_queries_generator)
