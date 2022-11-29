from pandas import concat, json_normalize


class Fields:
    def __init__(self, session):
        self._session = session

    def get_fields(self, **kwargs):

        params = {**kwargs}
        request = "fields.json"

        responses = self._session.get(request, params=params)

        r_n = [json_normalize(response, sep="_") for response in responses]
        df = concat(r_n)

        return df
