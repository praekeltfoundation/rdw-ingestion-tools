from api import concatenate_to_lazyframe
from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get_paginated
from ..schemas.messages import messages_schema


@define
class Messages:
    """Dedicated to the messages endpoint of the Turn BQ API"""

    client: Client

    def get_messages_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> LazyFrame:
        """Returns a Polars LazyFrame of Turn Messages by updated_at."""
        url = "messages/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        messages_generator = get_paginated(self.client, url, page_size=1000, **params)

        messages = concatenate_to_lazyframe(messages_generator, messages_schema)

        return messages
