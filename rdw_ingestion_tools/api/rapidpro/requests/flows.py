from attrs import define
from httpx import Client
from polars import LazyFrame

from api import concatenate_to_string_lazyframe

from ..extensions.httpx import get_paginated


@define
class Flows:
    """Dedicated to the flows endpoint of the Rapidpro API"""

    client: Client

    def get_flows(self, **kwargs: str | int) -> LazyFrame:
        """Get a Polars LazyFrame of Rapidpro flows.

        This endpoint does not support time-based filtering and
        can be called as:

        pyRapid.flows.get_flows()

        """
        url = "flows.json"

        flows_generator = get_paginated(self.client, url, **kwargs)

        flows = concatenate_to_string_lazyframe(
            flows_generator, object_columns=["labels", "results", "parent_refs"]
        )

        return flows
