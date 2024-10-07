from api import concatenate
from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


@define
class Chats:
    """Dedicated to the chats endpoint of the Turn BQ API"""

    client: Client

    def get_chats_by_id(self, chat_id: int) -> DataFrame:
        """Returns a pandas DataFrame of Turn Chats by chat_id"""

        url = f"chats/{chat_id}"

        chats_generator = get_paginated(
            self.client,
            url,
        )

        chats = concatenate(chats_generator)

        return chats

    def get_chats_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> DataFrame:
        """Returns a pandas DataFrame of Turn Chats by updated_at."""
        url = "chats/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        chats_generator = get_paginated(
            self.client, url, page_size=100, **params
        )

        chats = concatenate(chats_generator)

        return chats
