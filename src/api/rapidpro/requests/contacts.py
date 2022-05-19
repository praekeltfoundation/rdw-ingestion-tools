import pandas as pd


class Contacts:
    def __init__(self, session):
        self._session = session

    def get_contacts(self, **kwargs):

        params = {**kwargs}
        request = "contacts.json"

        responses = self._session.get(request, params=params)

        r_n = [pd.json_normalize(response, sep="_") for response in responses]
        df = pd.concat(r_n)

        return df
