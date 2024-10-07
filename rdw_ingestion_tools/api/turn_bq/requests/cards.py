from api import concatenate
from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


@define
class Cards:
    """Dedicated to the cards endpoint of the Turn BQ API"""

    client: Client

    def get_cards(self) -> DataFrame:
        """Returns a pandas DataFrame of Turn Cards"""

        url = "cards/"

        cards_generator = get_paginated(self.client, url)

        cards = concatenate(cards_generator)

        return cards

    def get_cards_by_id(self, card_id: int) -> DataFrame:
        """Returns a pandas DataFrame of Turn Cards by card_id"""

        url = f"cards/{card_id}"

        cards_generator = get_paginated(self.client, url)

        cards = concatenate(cards_generator)

        return cards
