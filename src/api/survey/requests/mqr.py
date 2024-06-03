from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


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
            self.client, url=url, start=ts, max_pages=max_pages
        )

        baseline_responses = []
        for item in baseline_generator:
            baseline_responses.append(json_normalize(item, sep="_"))

        try:
            baseline = concat(baseline_responses)
        except ValueError:
            baseline = DataFrame()

        return baseline
