from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


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

        contacts = concatenate(contacts_generator)

        return contacts
