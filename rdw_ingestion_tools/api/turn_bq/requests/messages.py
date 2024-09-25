from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class Messages:
    """Dedicated to the messages endpoint of the Turn BQ API"""

    client: Client

    def get_messages_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> DataFrame:
        """Returns a pandas DataFrame of Turn Messages by updated_at."""
        url = "messages/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        messages_generator = get_paginated(
            self.client, url, page_size=100, **params
        )

        try:
            messages = concat(
                [json_normalize(obj, sep="_") for obj in messages_generator]
            )
        except ValueError:
            messages = DataFrame()

        return messages
