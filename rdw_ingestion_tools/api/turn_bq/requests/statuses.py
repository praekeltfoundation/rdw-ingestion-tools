from api import concatenate
from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


@define
class Statuses:
    """Dedicated to the statuses endpoint of the Turn BQ API"""

    client: Client

    def get_statuses_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> DataFrame:
        """Returns a pandas DataFrame of Turn Statuses by updated_at."""
        url = "statuses/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        status_generator = get_paginated(
            self.client, url, page_size=100, **params
        )

        status = concatenate(status_generator)

        return status
