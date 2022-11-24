class Inbounds:
    def __init__(self, session):
        self._session = session

    def get_inbounds(self, **kwargs):

        url = "inbounds"

        response_list = self._session.get(url, **kwargs)

        return response_list
