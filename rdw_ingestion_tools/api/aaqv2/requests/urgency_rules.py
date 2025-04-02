from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


@define
class UrgencyRules:
    """Dedicated to the urgency-rules endpoint of the AAQ V2
    Data Export API.

    """

    client: Client

    def get_urgency_rules(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of urgency rules.

        No time-based query parameters are supported for this endpoint.
        Should return the full urgency rules  object or an empty DataFrame if
        no records are returned by the API.

        """

        url = "urgency-rules"

        urgency_rules_generator = get_paginated(self.client, url, **kwargs)

        return DataFrame(urgency_rules_generator)
