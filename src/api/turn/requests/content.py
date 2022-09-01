import pandas as pd


def deep_get(obj, path):
    if not path or not obj:
        return obj
    return deep_get(obj.get(path[0]), path[1:])


class Content:
    def __init__(self, session) -> None:
        self._session = session

    def get_content(self, start, end):

        url = "export"

        response = self._session.request("GET", url)
        response.raise_for_status()

        content = pd.json_normalize(response.json()["data"])

        return content
