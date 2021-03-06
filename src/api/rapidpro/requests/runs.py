import pandas as pd


class Runs:
    def __init__(self, session):
        self._session = session

    def get_runs(self, **kwargs):

        params = {**kwargs}
        request = "runs.json"

        responses = self._session.get(request, params=params)

        df = [pd.json_normalize(response, sep="_") for response in responses]

        del responses

        df = pd.concat(df)

        return df
