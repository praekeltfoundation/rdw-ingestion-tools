from ast import literal_eval

from attrs import define
from pandas import DataFrame, concat

from .. import BaseSession


@define
class Inbounds:
    """Dedicated to the inbounds endpoint of the AAQ Data Export API.

    This allows us to retrieve inbound messages sent to the IDI AAQ instance
    for a given project.

    Args:
       A BaseSession object.
    """

    base_session: type[BaseSession]

    def get_inbounds(self, **kwargs) -> DataFrame:
        """Get a pandas DataFrame of inbound messages.

        Args:
           **kwargs
           start_datetime: [via *kwargs] The start datetime query parameter to
              send. Example: '2020-01-01 00:00:00'
           end_datetime: [via **kwargs] The end datetime query parameter to
              send. Example: '2020-01-01 00:00:00'


        Returns:
           pandas.DataFrame
        """
        url = "inbounds"

        response_list = self.base_session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d} for d in response_list
        ]

        try:
            inbounds = concat([DataFrame(d, index=[0]) for d in response_list])
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                inbounds = DataFrame()

        return inbounds

    def get_faqranks(self, **kwargs) -> DataFrame:
        """Get a pandas DataFrame of faqranks for each inbound message.

        Args:
           **kwargs

        Returns:
           pandas.DataFrame
        """
        url = "inbounds"

        response_list = self.base_session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d} for d in response_list
        ]

        scores_list = []
        for response in response_list:
            scores = []
            id = response["inbound_id"]
            # We need to iterate over the model_scoring object.
            # This is a dict object that the API returns as str.
            model_scoring = literal_eval(response["model_scoring"])
            for faq in model_scoring:
                faqs = model_scoring[faq]
                if isinstance(faqs, str):
                    break
                rank = ""
                if "rank" in faqs:
                    rank = faqs["rank"]
                scores.append(
                    {
                        "inbound_id": id,
                        "faq_id": faq,
                        "score": faqs["overall_score"],
                        "rank": rank,
                    }
                )
            scores_list.append(DataFrame(scores))

        try:
            faq_ranks = concat(scores_list)
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                faq_ranks = DataFrame()

        return faq_ranks
