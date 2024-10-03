from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


@define
class UrgencyRules:
    """Dedicated to the urgency rules endpoint of the AAQ Data Export API.

    This allows us to retrieve different urgency rules that are implemented
    for a given AAQ instance.

    """

    client: Client

    def get_urgency_rules(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of urgency rules."""
        url = "urgency_rules"

        urgency_rules_generator = get_paginated(self.client, url, **kwargs)

        return DataFrame(urgency_rules_generator)
