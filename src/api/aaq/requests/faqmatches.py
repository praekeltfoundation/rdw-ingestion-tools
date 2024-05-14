from attrs import define
from pandas import DataFrame, concat

from .. import BaseSession


@define
class FAQMatches:
    """Dedicated to the faqmaches endpoint of the AAQ Data Export API.

    Args:
       A BaseSession object.
    """

    base_session: type[BaseSession]

    def get_faqmatches(self, **kwargs) -> DataFrame:
        """Get a pandas DataFrame of faqmatches.

        Args:
           **kwargs

        Returns:
           pandas.DataFrame
        """
        url = "faqmatches"

        response_list = self.base_session.get(url, **kwargs)

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
