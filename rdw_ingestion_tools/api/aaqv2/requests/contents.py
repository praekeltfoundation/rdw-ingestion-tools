from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


@define
class Contents:
    """Dedicated to the contents endpoint of the AAQ V2 Data Export API."""

    client: Client

    def get_faqmatches(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of contents.

        No time-based query parameters are supported for this endpoint.
        Should return the full contents object or an empty DataFrame if
        no records are returned by the API.

        """

        url = "contents"

        contents_generator = get_paginated(self.client, url, **kwargs)

        # IDI return weird stuff in the new API. Let's see if it
        # has what we need to convert to a df.
        return DataFrame(contents_generator)
