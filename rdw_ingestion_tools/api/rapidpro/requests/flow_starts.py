from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


@define
class FlowStarts:
    """Dedicated to the flowstarts endpoint of the Rapidpro API"""

    client: Client

    def get_flowstarts(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of Rapidpro flowstarts.

        This endpoint supports time-based filtering that allows
        to fetch results between two date parameters. Example:

        pyRapid.flowstarts.get_flowstarts(
            before="2023-01-02T00:00:00",
            after="2023-01-01T00:00:00"
            )

        """
        url = "flow_starts.json"

        flowstarts_generator = get_paginated(self.client, url, **kwargs)

        flowstarts = concatenate(flowstarts_generator)

        return flowstarts
