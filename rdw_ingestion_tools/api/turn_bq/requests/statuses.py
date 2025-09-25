from api import concatenate_to_lazyframe
from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get_paginated
from ..schemas.statuses import statuses_schema


@define
class Statuses:
    """Dedicated to the statuses endpoint of the Turn BQ API"""

    client: Client

    def get_statuses_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> LazyFrame:
        """Returns a Polars LazyFrame of Turn Statuses by updated_at."""
        url = "statuses/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        status_generator = get_paginated(self.client, url, page_size=1000, **params)

        status = concatenate_to_lazyframe(status_generator, statuses_schema)

        return status
