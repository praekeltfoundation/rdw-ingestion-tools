from ast import literal_eval

from attrs import define
from httpx import Client
from pandas import DataFrame, concat

from .. import get_paginated


@define
class Inbounds:
    """Dedicated to the inbounds endpoint of the AAQ Data Export API.

    This allows us to retrieve inbound messages sent to the IDI AAQ instance,
    the ranks of the various FAQ's as determined by the model for each inbound
    etc.

    """

    client: Client

    def get_inbounds(self, **kwargs) -> DataFrame:
        """Get a pandas DataFrame of inbound messages.

        This endpoint supports time-based query parameters which can
        be passed to this method as kwargs as in the following example:

        pyAAQ.inbounds.get_inbounds(
           start_datetime="2020-01-01 00:00:00",
           end_datetime="2020-12-31 00:00:00"
           )

        """
        url = "inbounds"

        response_list = get_paginated(client=self.client, url=url, **kwargs)

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

        This endpoint supports time-based query parameters which can
        be passed to this method as kwargs as in the following example:

        pyAAQ.inbounds.get_faqranks(
           start_datetime="2020-01-01 00:00:00",
           end_datetime="2020-12-31 00:00:00"
           )

        """
        url = "inbounds"

        response_list = get_paginated(client=self.client, url=url, **kwargs)

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
