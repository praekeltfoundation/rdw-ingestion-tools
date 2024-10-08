from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


@define
class PageViews:
    """Dedicated to the pageviews endpoint of the Content Repo API."""

    client: Client

    def get_pageviews(self, ts: str, max_pages: int = 5) -> DataFrame:
        """Get a pandas DataFrame of pageviews.

        API only accepts initial timestamp and returns records after.
        Example usage as follows:

        start_time = datetime(2024, 1, 1).isoformat()
        pageviews = pyContent.pageviews.get_pageviews(ts=start_time)

        """

        url = f"custom/pageviews/?timestamp_gt={ts}"

        pageviews_generator = get_paginated(
            client=self.client, url=url, max_pages=max_pages
        )

        pageviews = concatenate(pageviews_generator)

        return pageviews
