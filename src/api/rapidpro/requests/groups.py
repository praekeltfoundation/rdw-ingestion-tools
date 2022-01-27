import json

import pandas as pd


class Groups:
    def __init__(self, session):
        self._session = session

    def get_groups(self, **kwargs):

        params = {**kwargs}
        request = "groups.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)

        return df
