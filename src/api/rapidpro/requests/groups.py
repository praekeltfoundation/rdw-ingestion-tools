from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class Groups:
    """Dedicated to the groups endpoint of the Rapidpro API"""

    client: Client

    def get_groups(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of Rapidpro groups.

        This endpoint does not support time-based filtering and
        can be called as:

        pyRapid.groups.get_groups()

        """
        url = "groups.json"

        groups_generator = get_paginated(client=self.client, url=url, **kwargs)

        groups_list: list[DataFrame] = [
            json_normalize(response, sep="_") for response in groups_generator
        ]

        try:
            groups = concat(groups_list)
        except ValueError:
            groups = DataFrame()

        return groups
