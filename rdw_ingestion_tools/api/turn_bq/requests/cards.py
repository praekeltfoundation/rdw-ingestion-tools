from api import concatenate_to_lf
from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get_paginated
from ..schemas.cards import cards_schema


@define
class Cards:
    """Dedicated to the cards endpoint of the Turn BQ API"""

    client: Client

    def get_cards(self) -> LazyFrame:
        """Returns a pandas DataFrame of Turn Cards"""

        url = "cards/"

        cards_generator = get_paginated(self.client, url)

        cards = concatenate_to_lf(cards_generator, cards_schema)

        return cards

    def get_cards_by_id(self, card_id: int) -> LazyFrame:
        """Returns a pandas DataFrame of Turn Cards by card_id"""

        url = f"cards/{card_id}"

        cards_generator = get_paginated(self.client, url)

        cards = concatenate_to_lf(cards_generator, cards_schema)

        return cards
