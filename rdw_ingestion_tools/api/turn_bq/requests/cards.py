from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class Cards:
    """Dedicated to the cards endpoint of the Turn BQ API"""

    client: Client

    def get_cards(self) -> DataFrame:
        """Returns a pandas DataFrame of Turn Cards"""
        url = "cards"

        cards_generator = get_paginated(self.client, url)

        try:
            cards = concat(
                [json_normalize(obj, sep="_") for obj in cards_generator]
            )
        except ValueError:
            cards = DataFrame()

        return cards
