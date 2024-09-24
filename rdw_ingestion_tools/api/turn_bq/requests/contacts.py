from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class Contacts:
    """Dedicated to the contacts endpoint of the Turn BQ API"""

    client: Client

    def get_contacts_by_id(self, contact_id: int) -> DataFrame:
        """Returns a pandas DataFrame of Turn Contacts by contact_id"""

        url = f"contacts/{contact_id}"

        contacts_generator = get_paginated(
            self.client,
            url,
        )

        try:
            contacts = concat(
                [json_normalize(obj, sep="_") for obj in contacts_generator]
            )
        except ValueError:
            contacts = DataFrame()

        return contacts

    def get_contacts_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> DataFrame:
        """Returns a pandas DataFrame of Turn Contacts by updated_at."""
        url = "contacts/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        contacts_generator = get_paginated(
            self.client, url, page_size=100, **params
        )

        try:
            contacts = concat(
                [json_normalize(obj, sep="_") for obj in contacts_generator]
            )
        except ValueError:
            contacts = DataFrame()

        return contacts
