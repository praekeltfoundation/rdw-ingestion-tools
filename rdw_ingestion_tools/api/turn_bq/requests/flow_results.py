from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class FlowResults:
    """
    Dedicated to the flow results endpoint of the
    Turn BQ API

    """

    client: Client

    def get_flow_results_by_id(self, stack_uuid: int) -> DataFrame:
        """
        Returns a pandas DataFrame of Turn Flow Results
        by stack_uuid

        """

        url = f"flow_results/{stack_uuid}"

        flow_results_generator = get_paginated(
            self.client,
            url,
        )

        try:
            flow_results = concat(
                [
                    json_normalize(obj, sep="_")
                    for obj in flow_results_generator
                ]
            )
        except ValueError:
            flow_results = DataFrame()

        return flow_results

    def get_flow_results_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> DataFrame:
        """
        Returns a pandas DataFrame of Turn Flow Results
        by updated_at.

        """

        url = "flow_results/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        flow_results_generator = get_paginated(
            self.client, url, page_size=100, **params
        )

        try:
            flow_results = concat(
                [
                    json_normalize(obj, sep="_")
                    for obj in flow_results_generator
                ]
            )
        except ValueError:
            flow_results = DataFrame()

        return flow_results