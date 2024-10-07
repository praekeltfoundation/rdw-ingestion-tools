from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


@define
class Runs:
    """Dedicated to the runs endpoint of the Rapidpro API"""

    client: Client

    def get_runs(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of Rapidpro runs.

        This endpoint supports time-based filtering that allows
        to fetch results between two date parameters. Example:

        pyRapid.runs.get_runs(
            before="2023-01-02T00:00:00",
            after="2023-01-01T00:00:00"
            )

        """
        url = "runs.json"

        runs_generator = get_paginated(self.client, url, **kwargs)

        runs = concatenate(runs_generator)

        return runs
