from attrs import define
from httpx import Client
from pandas import DataFrame, concat

from .. import get_paginated


@define
class FAQMatches:
    """Dedicated to the faqmatches endpoint of the AAQ Data Export API."""

    client: Client

    def get_faqmatches(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of faqmatches.

        No time-based query parameters are supported for this endpoint.
        Should return the full faqmatches object or an empty DataFrame if
        no records are returned by the API.

        """

        url = "faqmatches"

        """
        Open issue in mypy means we need to set defaults here to stop
        mypy from complaining: https://github.com/python/mypy/issues/1969

        """
        response_list = get_paginated(
            client=self.client, url=url, limit=100, offset=0, **kwargs
        )

        try:
            faqmatches = concat(
                [DataFrame(d, index=[0]) for d in response_list]
            )
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                faqmatches = DataFrame()

        return faqmatches
