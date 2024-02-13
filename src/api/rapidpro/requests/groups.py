from pandas import concat, json_normalize


class Groups:
    def __init__(self, session):
        self._session = session

    def get_groups(self, **kwargs):
        params = {**kwargs}
        request = "groups.json"

        responses = self._session.get(request, params=params)

        r_n = [json_normalize(response, sep="_") for response in responses]
        df = concat(r_n)

        return df
