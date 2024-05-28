from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class PageViews:
    """Dedicated to the pageviews endpoint of the Content Repo API."""

    client: Client

    def get_pageviews(self, ts: str, max_pages: int = 5) -> DataFrame:
        """Get a pandas DataFrame of pageviews.

        API only accepts initial timestamp and returns records after.
        Example usage as follows:

        start_time = datetime.strptime("2024-01-01", "%Y-%m-%d").isoformat()
        pageviews = pyContent.pageviews.get_pageviews(ts=start_time)

        """

        url = "custom/pageviews/?timestamp_gt=" + ts

        pageviews_generator = get_paginated(
            client=self.client, url=url, max_pages=max_pages
        )

        pageviews_list: list[DataFrame] = [
            json_normalize(response, sep="_")
            for response in pageviews_generator
        ]

        try:
            pageviews = concat(pageviews_list)
        except ValueError:
            pageviews = DataFrame()

        return pageviews
