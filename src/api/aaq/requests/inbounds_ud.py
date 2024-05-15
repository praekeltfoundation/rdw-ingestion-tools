from attrs import define
from pandas import DataFrame, concat

from .. import BaseSession


@define
class InboundsUD:
    """Dedicated to the inbounds_ud endpoint of the AAQ Data Export API.

    This allows us to retrieve data on urgency detection rules associated
    with different inbound messages.

    Args:
       base_session: a BaseSession object.
    """

    base_session: type[BaseSession]

    def get_inbounds_ud(self, **kwargs) -> DataFrame:
        """Get inbounds from the urgency detection endpoint.

        Args:
           **kwargs
           start_datetime: [via *kwargs] The start datetime query parameter to
              send. Example: '2020-01-01 00:00:00'
           end_datetime: [via **kwargs] The end datetime query parameter to
              send. Example: '2020-01-01 00:00:00'

        Returns:
           pandas.DataFrame
        """

        url = "inbounds_ud"

        response_list = self.base_session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d} for d in response_list
        ]

        try:
            inbounds_ud = concat(
                [DataFrame(d, index=[0]) for d in response_list]
            )
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                inbounds_ud = DataFrame()

        return inbounds_ud
