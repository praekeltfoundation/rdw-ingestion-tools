from attrs import define
from httpx import Client
from polars import LazyFrame

from api import concatenate_to_string_lazyframe

from ..extensions.httpx import get_paginated


@define
class Fields:
    """Dedicated to the fields endpoint of the Rapidpro API"""

    client: Client

    def get_fields(self, **kwargs: str | int) -> LazyFrame:
        """Get a polars LazyFrame of Rapidpro fields.

        This endpoint does not support time-based filtering and
        can be called as:

        pyRapid.fields.get_fields()

        """
        url = "fields.json"

        fields_generator = get_paginated(self.client, url, **kwargs)

        fields = concatenate_to_string_lazyframe(fields_generator, object_columns=[])

        return fields
