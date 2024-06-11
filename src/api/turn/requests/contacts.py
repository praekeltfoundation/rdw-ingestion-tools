from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class Contacts:
    """Dedicated to the contacts endpoint of the Turn Data Export API."""

    client: Client

    def get_contacts(
        self, start: str, end: str, **kwargs: str | int
    ) -> DataFrame:
        """Returns a pandas DataFrame of Turn Contacts.

        The endpoint supports time-base query parameters and
        can be called as:

        pyTurn.contacts.get_contacts(
            start=start,
            end=end
            )

        See examples/turn/contacts.py for information on
        timestamp formatting. (The Turn Data Export API is
        pedantic on such issues).

        """
        url = "data/contacts"

        contacts_generator = get_paginated(
            self.client, url, start=start, end=end, **kwargs
        )

        try:
            contacts = concat(
                [json_normalize(obj, sep="_") for obj in contacts_generator]
            )
        except ValueError:
            contacts = DataFrame()

        return contacts
