from attrs import define
from pandas import DataFrame, concat

from .. import BaseSession


@define
class UrgencyRules:
    """Dedicated to the urgency rules endpoint of the AAQ Data Export API.

    This allows us to retrieve different urgency rules that are implemented
    for a given AAQ instance.

    Args:
       A BaseSession object.
    """

    base_session: type[BaseSession]

    def get_urgency_rules(self, **kwargs) -> DataFrame:
        """Get a pandas DataFrame of urgency rules.

        Args:
           **kwargs

        Returns:
           pandas.DataFrame
        """
        url = "urgency_rules"

        response_list = self.base_session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d} for d in response_list
        ]

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
