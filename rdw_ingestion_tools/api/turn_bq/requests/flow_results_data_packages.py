from api import concatenate_to_lf
from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get_paginated
from ..schemas.flow_results_data_packages import flow_results_data_packages_schema


@define
class FlowResultsDataPackages:
    """
    Dedicated to the flow results data packages endpoint of the
    Turn BQ API

    """

    client: Client

    def get_flow_results_data_packages_by_id(self, stack_uuid: int) -> LazyFrame:
        """
        Returns a pandas DataFrame of Turn Flow Results Data Packages
        by stack_uuid

        """

        url = f"flow_results_data_packages/{stack_uuid}"

        flow_results_data_packages_generator = get_paginated(
            self.client,
            url,
        )

        flow_results_data_packages = concatenate_to_lf(
            flow_results_data_packages_generator, flow_results_data_packages_schema
        )

        return flow_results_data_packages

    def get_flow_results_data_packages_by_updated_at(
        self, from_timestamp: str, to_timestamp: str
    ) -> LazyFrame:
        """
        Returns a pandas DataFrame of Turn Flow Results Data Packages
        by updated_at.

        """

        url = "flow_results_data_packages/"

        params = {
            "from_timestamp": from_timestamp,
            "to_timestamp": to_timestamp,
        }

        flow_results_data_packages_generator = get_paginated(
            self.client, url, page_size=1000, **params
        )

        flow_results_data_packages = concatenate_to_lf(
            flow_results_data_packages_generator, flow_results_data_packages_schema
        )

        return flow_results_data_packages
