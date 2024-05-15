from attrs import define
from pandas import DataFrame, concat

from .. import BaseClient


@define
class FAQMatches:
    """Dedicated to the faqmatches endpoint of the AAQ Data Export API."""

    base_client: type[BaseClient]

    def get_faqmatches(self, **kwargs) -> DataFrame:
        """Get a pandas DataFrame of faqmatches.

        No time-based query parameters are supported for this endpoint.
        Should return the full faqmatches object or an empty DataFrame if
        no records are returned by the API.

        """

        url = "faqmatches"

        response_list = self.base_client.paginate_get(url, **kwargs)

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
