from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


# @define
# class FAQMatches:
#     """Dedicated to the faqmatches endpoint of the AAQ Data Export API."""

#     client: Client

#     def get_faqmatches(self, **kwargs: str | int) -> DataFrame:
#         """Get a pandas DataFrame of faqmatches.

#         No time-based query parameters are supported for this endpoint.
#         Should return the full faqmatches object or an empty DataFrame if
#         no records are returned by the API.

#         """

#         url = "faqmatches"

#         faqmatches_generator = get_paginated(self.client, url, **kwargs)

#         return DataFrame(faqmatches_generator)

@define
class NewEndpointThingie:
    client: Client
