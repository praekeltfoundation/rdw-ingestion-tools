from api import concatenate_to_lazyframe
from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get_paginated
from ..schemas.chats import chats_schema


@define
class Chats:
    """Dedicated to the chats endpoint of the Turn BQ API"""

    client: Client

    def get_chats_by_id(self, chat_id: int) -> LazyFrame:
        """Returns a Polars LazyFrame of Turn Chats by chat_id"""

        url = f"chats/{chat_id}"

        chats_generator = get_paginated(
            self.client,
            url,
        )

        chats = concatenate_to_lazyframe(chats_generator, chats_schema)

        return chats

    def get_chats_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> LazyFrame:
        """Returns a Polars LazyFrame of Turn Chats by updated_at."""
        url = "chats/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        chats_generator = get_paginated(self.client, url, page_size=1000, **params)

        chats = concatenate_to_lazyframe(chats_generator, chats_schema)

        return chats
