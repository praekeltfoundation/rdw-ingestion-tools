import json

import pandas as pd


class Fields:
    def __init__(self, session):
        self._session = session

    def get_fields(self, **kwargs):

        params = {**kwargs}
        request = "fields.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)

        return df
