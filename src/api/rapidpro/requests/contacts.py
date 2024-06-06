from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class Contacts:
    """Dedicated to the contacts endpoint of the Rapidpro API"""

    client: Client

    def get_contacts(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of Rapidpro contacts.

        This endpoint supports time-based filtering that allows
        to fetch results between two date parameters. Example:

        pyRapid.contacts.get_contacts(
            before="2023-01-02T00:00:00",
            after="2023-01-01T00:00:00"
            )

        """
        url = "contacts.json"

        contacts_generator = get_paginated(self.client, url, **kwargs)

        contacts_list: list[DataFrame] = [
            json_normalize(response, sep="_")
            for response in contacts_generator
        ]

        try:
            contacts = concat(contacts_list)
        except ValueError:
            contacts = DataFrame()

        return contacts
