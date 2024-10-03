from attrs import define
from httpx import Client
from pandas import DataFrame, concat, json_normalize

from ..extensions.httpx import get_paginated


@define
class Messages:
    """Dedicated to the messages endpoint of the Turn Data Export API."""

    client: Client

    def get_messages(
        self, start: str, end: str, **kwargs: str | int
    ) -> dict[str, DataFrame]:
        """Get a dict of pandas DataFrames for inbound and outbound messages.

        This endpoint supports time-based filtering that allows you to
        fetch results between two different start and end dates.

        pyTurn.messages.get_messages(
            start=start,
            end=end
            )

        See examples/turn/messages.py.

        """

        url = "data/messages"

        messages_generator = get_paginated(
            self.client, url, start=start, end=end, **kwargs
        )

        contacts, inbound_messages, outbound_messages = [], [], []
        for obj in messages_generator:
            if "_vnd" not in obj:
                contacts.append(json_normalize(obj["contacts"], sep="_"))
                inbound_messages.append(
                    json_normalize(obj["messages"], sep="_")
                )
            else:
                outbound_messages.append(json_normalize(obj, sep="_"))

        try:
            df_inbound = concat(
                [concat(contacts), concat(inbound_messages)], axis=1
            )
        except ValueError:
            df_inbound = DataFrame()

        try:
            df_outbound = concat(outbound_messages)
        except ValueError:
            df_outbound = DataFrame()

        return {"inbound": df_inbound, "outbound": df_outbound}
