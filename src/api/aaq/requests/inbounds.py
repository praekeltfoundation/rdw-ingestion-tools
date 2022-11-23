class Inbounds:
    def __init__(self, session):
        self._session = session

    def get_inbounds(self, start, end):

        url = "inbounds"

        data = {"start_datetime": start, "end_datetime": end}

        cursor_request = self._session.request("GET", url, params=data)

        return cursor_request
