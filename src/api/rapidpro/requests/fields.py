from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


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

        params = {**kwargs}
        url = "fields.json"

        fields_generator = get_paginated(client=self.client, url=url, **kwargs)

        fields_list: list[DataFrame] = [
            json_normalize(response, sep="_") for response in fields_generator
        ]

        try:
            fields = concat(fields_list)
        except ValueError:
            fields = DataFrame()

        return fields
