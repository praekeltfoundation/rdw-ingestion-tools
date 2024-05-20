from attrs import define
from httpx import Client
from pandas import DataFrame, concat

from .. import get_paginated


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

        """
        See faqmatches.py for context on usage of defaults.

        """
        response_list = get_paginated(
            client=self.client, url=url, limit=100, offset=0, **kwargs
        )

        try:
            urgency_rules = concat(
                [DataFrame(d, index=[0]) for d in response_list]
            )
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                urgency_rules = DataFrame()

        return urgency_rules
