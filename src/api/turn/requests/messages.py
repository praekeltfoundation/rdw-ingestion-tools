import json

import pandas as pd
from pandas.core.reshape.concat import concat


def deep_get(obj, path):
    if not path or not obj:
        return obj
    return deep_get(obj.get(path[0]), path[1:])


class Messages:
    def __init__(self, session):
        self._session = session

    def get_messages(self, start, end):

        url = "messages/cursor"

        data = {"from": start, "until": end}

        cursor_request = self._session.request("POST", url, json=data)

        cursor_request.raise_for_status()
        cursor = cursor_request.json()["cursor"]

        l = []
        i = 0
        while cursor:
            i += 1
            print("Iteration #: ", i)
            response = self._session.request("GET", url + f"/{cursor}")
            response.raise_for_status()
            for row in response.json()["data"]:
                l.append(row)

            cursor = deep_get(response.json(), ["paging", "next"])

        contacts, inbound_messages, outbound_messages = [], [], []
        for obj in l:
            if "_vnd" not in obj.keys():
                contacts.append(pd.json_normalize(obj["contacts"], sep="_"))
                inbound_messages.append(pd.json_normalize(obj["messages"], sep="_"))
            elif "_vnd" in obj.keys():
                outbound_messages.append(pd.json_normalize(obj, sep="_"))

        try:
            df_inbound = pd.concat(
                [pd.concat(contacts), pd.concat(inbound_messages)], axis=1
            )
        except ValueError:
            df_inbound = pd.DataFrame()

        try:
            df_outbound = pd.concat(outbound_messages)
        except ValueError:
            df_outbound = pd.DataFrame()

        return {"inbound": df_inbound, "outbound": df_outbound}
