from attrs import define
from httpx import Client
from polars import LazyFrame

from api import concatenate_to_string_lazyframe

from ..extensions.httpx import get_paginated


@define
class Runs:
    """Dedicated to the runs endpoint of the Rapidpro API"""

    client: Client

    def get_runs(
        self, start_datetime: str, end_datetime: str, **kwargs: str | int
    ) -> LazyFrame:
        """Get a Polars LazyFrame of Rapidpro runs.

        This endpoint supports time-based filtering that allows
        to fetch results between two date parameters. Example:

        pyRapid.runs.get_runs(
            end_datetime="2023-01-02T00:00:00",
            start_datetime="2023-01-01T00:00:00"
            )

        """
        url = "runs.json"

        runs_generator = get_paginated(
            self.client, url, after=start_datetime, before=end_datetime, **kwargs
        )

        runs = concatenate_to_string_lazyframe(
            objs=runs_generator, object_columns=["path", "flow", "contact", "events"]
        )

        return runs
