from attrs import define
from httpx import Client
from polars import LazyFrame

from api import concatenate_to_string_lazyframe

from ..extensions.httpx import get_paginated


@define
class Groups:
    """Dedicated to the groups endpoint of the Rapidpro API"""

    client: Client

    def get_groups(self, **kwargs: str | int) -> LazyFrame:
        """Get a Polars LazyFrame of Rapidpro groups.

        This endpoint does not support time-based filtering and
        can be called as:

        pyRapid.groups.get_groups()

        """
        url = "groups.json"

        groups_generator = get_paginated(self.client, url, **kwargs)

        groups = concatenate_to_string_lazyframe(groups_generator, object_columns=[])

        return groups
