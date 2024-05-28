from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from .. import get_paginated


@define
class Pages:
    """Dedicated to the Pages endpoint of the Content Repo API"""

    client: Client

    def get_pages(self, max_pages: int = 5) -> DataFrame:
        """Get a pandas DataFrame of Content Repo pages.

        No time-based query parameters are supported by the endpoint.
        Full set of pages accessible via pagination.

        """

        url = "pages"

        pages_generator = get_paginated(
            client=self.client,
            url=url,
            max_pages=max_pages,
        )

        pages_list: list[DataFrame] = [
            json_normalize(response, sep="_") for response in pages_generator
        ]

        try:
            pages = concat(pages_list)
        except ValueError:
            pages = DataFrame()

        return pages
