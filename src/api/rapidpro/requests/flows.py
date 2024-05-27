from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


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

        params = {**kwargs}
        url = "flows.json"

        flows_generator = get_paginated(client=self.client, url=url, **kwargs)

        flows_list: list[DataFrame] = [
            json_normalize(response, sep="_") for response in flows_generator
        ]

        try:
            flows = concat(flows_list)
        except ValueError:
            flows = DataFrame()

        return flows
