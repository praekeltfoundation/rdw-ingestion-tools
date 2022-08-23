import pandas as pd


def deep_get(obj, path):
    if not path or not obj:
        return obj
    return deep_get(obj.get(path[0]), path[1:])


class Contacts:
    def __init__(self, session):
        self._session = session

    def get_contacts(self, start, end):

        url = "contacts/cursor"

        data = {"from": start, "until": end}

        cursor_request = self._session.request("POST", url, json=data)

        cursor_request.raise_for_status()
        cursor = cursor_request.json()["cursor"]

        response_list = []
        i = 0
        while cursor:
            i += 1
            print("Iteration #: ", i)
            response = self._session.request("GET", url + f"/{cursor}")
            response.raise_for_status()
            for row in response.json()["data"]:
                response_list.append(row)

            cursor = deep_get(response.json(), ["paging", "next"])

        contacts = pd.concat(
            [pd.json_normalize(obj, sep="_") for obj in response_list]
        )

        return contacts
