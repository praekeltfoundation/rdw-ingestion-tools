from pandas import concat, json_normalize


class Runs:
    def __init__(self, session):
        self._session = session

    def get_runs(self, **kwargs):

        params = {**kwargs}
        request = "runs.json"

        responses = self._session.get(request, params=params)

        df = [json_normalize(response, sep="_") for response in responses]

        del responses

        df = concat(df)

        return df
