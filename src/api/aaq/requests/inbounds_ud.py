from pandas import DataFrame, concat


class InboundsUD:
    def __init__(self, session) -> None:
        self._session = session

    def get_inbounds_ud(self, **kwargs):
        url = "inbounds_ud"

        response_list = self._session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d} for d in response_list
        ]

        try:
            inbounds_ud = concat(
                [DataFrame(d, index=[0]) for d in response_list]
            )
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                inbounds_ud = DataFrame()

        return inbounds_ud
