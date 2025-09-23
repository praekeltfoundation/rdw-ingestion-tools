from attrs import define
from httpx import Client
from polars import LazyFrame

from api import concatenate_to_string_lazyframe

from ..extensions.httpx import get_paginated


@define
class Contacts:
    """Dedicated to the contacts endpoint of the Rapidpro API"""

    client: Client

    def get_contacts(
        self, start_datetime: str, end_datetime: str, **kwargs: str | int
    ) -> LazyFrame:
        """Get a Polars LazyFrame of Rapidpro contacts.

        This endpoint supports time-based filtering that allows
        to fetch results between two date parameters. Example:

        pyRapid.contacts.get_contacts(
            end_datetime="2023-01-02T00:00:00",
            start_datetime="2023-01-01T00:00:00"
            )

        """
        url = "contacts.json"

        contacts_generator = get_paginated(
            self.client, url, after=start_datetime, before=end_datetime, **kwargs
        )

        contacts = concatenate_to_string_lazyframe(
            contacts_generator, object_columns=["urns", "groups"]
        )

        return contacts
