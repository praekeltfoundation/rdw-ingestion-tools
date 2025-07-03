from api import concatenate_to_lf
from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get_paginated
from ..schemas.contacts import contacts_schema


@define
class Contacts:
    """Dedicated to the contacts endpoint of the Turn BQ API"""

    client: Client

    def get_contacts_by_id(self, contact_id: int) -> LazyFrame:
        """Returns a pandas DataFrame of Turn Contacts by contact_id"""

        url = f"contacts/{contact_id}"

        contacts_generator = get_paginated(
            self.client,
            url,
        )

        contacts = concatenate_to_lf(contacts_generator, contacts_schema)

        return contacts

    def get_contacts_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> LazyFrame:
        """Returns a pandas DataFrame of Turn Contacts by updated_at."""
        url = "contacts/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        contacts_generator = get_paginated(self.client, url, page_size=1000, **params)

        contacts = concatenate_to_lf(contacts_generator, contacts_schema)

        return contacts
