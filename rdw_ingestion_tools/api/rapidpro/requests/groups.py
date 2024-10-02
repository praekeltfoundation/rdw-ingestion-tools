from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.dataframe import concatenate
from ..extensions.httpx import get_paginated


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

        groups_generator = get_paginated(self.client, url, **kwargs)

        groups = concatenate(groups_generator)

        return groups
