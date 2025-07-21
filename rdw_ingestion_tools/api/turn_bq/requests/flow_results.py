from api import concatenate_to_lf
from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get_paginated
from ..schemas.flow_results import flow_results_schema


@define
class FlowResults:
    """
    Dedicated to the flow results endpoint of the
    Turn BQ API

    """

    client: Client

    def get_flow_results_by_id(self, stack_uuid: int) -> LazyFrame:
        """
        Returns a pandas DataFrame of Turn Flow Results
        by stack_uuid

        """

        url = f"flow_results/{stack_uuid}"

        flow_results_generator = get_paginated(
            self.client,
            url,
        )

        flow_results = concatenate_to_lf(flow_results_generator, flow_results_schema)

        return flow_results

    def get_flow_results_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> LazyFrame:
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
            self.client, url, page_size=1000, **params
        )

        flow_results = concatenate_to_lf(flow_results_generator, flow_results_schema)

        return flow_results
