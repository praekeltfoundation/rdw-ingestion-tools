from attrs import define
from httpx import Client
from pandas import DataFrame, concat

from .. import paginate_get


@define
class FAQMatches:
    """Dedicated to the faqmatches endpoint of the AAQ Data Export API."""

    httpx_client: Client

    def get_faqmatches(self, **kwargs) -> DataFrame:
        """Get a pandas DataFrame of faqmatches.

        No time-based query parameters are supported for this endpoint.
        Should return the full faqmatches object or an empty DataFrame if
        no records are returned by the API.

        """

        url = "faqmatches"

        response_list = paginate_get(
            httpx_client=self.httpx_client, url=url, **kwargs
        )

        response_list = [
            {key: str(d[key]) for key in d} for d in response_list
        ]

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
