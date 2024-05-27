from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


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

        runs_generator = get_paginated(client=self.client, url=url, **kwargs)

        runs_list: list[DataFrame] = [
            json_normalize(response, sep="_") for response in runs_generator
        ]

        try:
            runs = concat(runs_list)
        except ValueError:
            runs = DataFrame()

        return runs
