from collections.abc import Iterator
from typing import TypedDict

from attrs import define
from httpx import Client
from pandas import DataFrame

from ..extensions.httpx import get_paginated


class FAQModel(TypedDict):
    faq_title: str
    overall_score: str
    rank: str | None
    faq_content_to_send: str | None
    tag_cs: str | None


class FAQRank(TypedDict):
    faq_id: str
    score: str
    rank: str | None


def build_faqranks(
    model_scoring_dict: dict[str, str | FAQModel],
) -> Iterator[FAQRank]:
    """Extracts important information from the AAQ model scoring dict.

    Each inbound message contains a dict that contains the model scores
    for every other faq not returned to the user. This function will
    traverse this dict, look for nested dicts, and return only the
    important information we care about for faqranks.

    """
    for k, v in model_scoring_dict.items():
        if not isinstance(v, str):
            rank = v.get("rank", "")
            yield {
                "faq_id": k,
                "score": v["overall_score"],
                "rank": rank,
            }


@define
class Inbounds:
    """Dedicated to the inbounds endpoint of the AAQ Data Export API.

    This allows us to retrieve inbound messages sent to the IDI AAQ instance,
    the ranks of the various FAQ's as determined by the model for each inbound
    etc.

    """

    client: Client

    def get_inbounds(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of inbound messages.

        This endpoint supports time-based query parameters which can
        be passed to this method as kwargs as in the following example:

        pyAAQ.inbounds.get_inbounds(
           start_datetime="2020-01-01 00:00:00",
           end_datetime="2020-12-31 00:00:00"
           )

        """
        url = "inbounds"

        inbounds_generator = get_paginated(self.client, url, **kwargs)

        return DataFrame(inbounds_generator)

    def get_faqranks(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of faqranks for each inbound message.

        This endpoint supports time-based query parameters which can
        be passed to this method as kwargs as in the following example:

        pyAAQ.inbounds.get_faqranks(
           start_datetime="2023-01-01 00:00:00",
           end_datetime="2023-12-31 00:00:00"
           )

        """
        inbounds = self.get_inbounds(**kwargs)

        faq_ranks_list = []
        for _idx, row in inbounds.iterrows():
            for faqrank in build_faqranks(dict(row["model_scoring"])):
                faq_ranks_list.append({"inbound_id": row["inbound_id"], **faqrank})

        return DataFrame(faq_ranks_list)
