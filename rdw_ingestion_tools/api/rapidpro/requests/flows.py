from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


@define
class Flows:
    """Dedicated to the flows endpoint of the Rapidpro API"""

    client: Client

    def get_flows(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of Rapidpro flows.

        This endpoint does not support time-based filtering and
        can be called as:

        pyRapid.flows.get_flows()

        """
        url = "flows.json"

        flows_generator = get_paginated(self.client, url, **kwargs)

        flows = concatenate(flows_generator)

        return flows
