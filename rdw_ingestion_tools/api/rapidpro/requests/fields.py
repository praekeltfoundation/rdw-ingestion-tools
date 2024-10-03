from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


@define
class Fields:
    """Dedicated to the fields endpoint of the Rapidpro API"""

    client: Client

    def get_fields(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of Rapidpro fields.

        This endpoint does not support time-based filtering and
        can be called as:

        pyRapid.fields.get_fields()

        """
        url = "fields.json"

        fields_generator = get_paginated(self.client, url, **kwargs)

        fields = concatenate(fields_generator)

        return fields
