from pandas import DataFrame, concat


class Inbounds:
    def __init__(self, session):
        self._session = session

    def get_inbounds(self, **kwargs):

        url = "inbounds"

        response_list = self._session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d.keys()} for d in response_list
        ]

        try:
            inbounds = concat([DataFrame(d, index=[0]) for d in response_list])
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                inbounds = DataFrame()

        return inbounds
