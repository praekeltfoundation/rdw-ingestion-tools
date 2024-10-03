from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


@define
class MQR:
    """Dedicated to the baseline endpoint of the MQR custom survey API."""

    client: Client

    def get_baseline(self, ts: str, max_pages: int = 5) -> DataFrame:
        """
        API only accepts initial timestamp and returns records after.

        pySurvey.mqr.get_baseline(ts=start)

        """

        url = "mqrbaselinesurvey/"

        baseline_generator = get_paginated(
            self.client, url, start=ts, max_pages=max_pages
        )

        baseline = concatenate(baseline_generator)

        return baseline
