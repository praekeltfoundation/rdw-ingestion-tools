class InboundsUD:
    def __init__(self, session) -> None:
        self._session = session

    def get_inbounds_ud(self, **kwargs):

        url = "inbounds_ud"

        response_list = self._session.get(url, **kwargs)

        return response_list
