from attrs import define
from httpx import Client
from pandas import DataFrame

from .. import get_paginated


@define
class InboundsUD:
    """Dedicated to the inbounds_ud endpoint of the AAQ Data Export API.

    This allows us to retrieve data on urgency detection rules associated
    with different inbound messages.

    """

    client: Client

    def get_inbounds_ud(self, **kwargs: str | int) -> DataFrame:
        """Get inbounds from the urgency detection endpoint.

        This endpoint supports time-based query parameters which can be
        passed to this method as kwargs as in the following example:

        pyAAQ.inbounds.get_inbounds_ud(
           start_datetime="2020-01-01 00:00:00",
           end_datetime="2020-12-31 00:00:00"
           )

        """

        url = "inbounds_ud"

        """
        See faqmatches.py for context on usage of defaults.

        """
        inbounds_ud_generator = get_paginated(
            client=self.client, url=url, limit=100, offset=0, **kwargs
        )

        return DataFrame(inbounds_ud_generator)
