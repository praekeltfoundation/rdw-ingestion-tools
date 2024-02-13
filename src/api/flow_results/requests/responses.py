import time
from urllib.parse import urlencode


class Responses:
    def __init__(self, session):
        self._session = session

    @staticmethod
    def _parse_response_pagination_link(link):
        link_split = link.split("packages/")[-1]
        return link_split

    def get_ids(self, **kwargs):
        params = {**kwargs}

        request = ""

        response = self._session.get(request, params=params)
        response.raise_for_status()

        ids = [flow["id"] for flow in response.json()["data"]]

        return ids

    def get(self, start_time, end_time, max_retries=3, **kwargs):
        ids = self.get_ids()

        params = {}

        filters = urlencode(
            {
                "filter[start-timestamp]": start_time,
                "filter[end-timestamp]": end_time,
                **kwargs,
            }
        )

        responses = []

        for id in ids:
            retries = 0
            request = f"{id}/responses/" + "?" + filters
            while request and retries <= max_retries:
                response = self._session.get(request, params=params)
                if response.ok:
                    data = response.json()
                    for res in data["data"]["attributes"]["responses"]:
                        tmp = res
                        tmp.insert(0, id)
                        responses.append(tmp)
                    request = data["data"]["relationships"]["links"]["next"]
                    if request:
                        request = self._parse_response_pagination_link(request)
                    else:
                        pass
                elif not response.ok and retries < max_retries:
                    time.sleep(1)
                    retries += 1
                elif not response.ok and retries == max_retries:
                    request = None

        r_data = {
            "flow_id": [response[0] for response in responses],
            "timestamp": [response[1] for response in responses],
            "row_id": [response[2] for response in responses],
            "contact_id": [response[3] for response in responses],
            "session_id": [response[4] for response in responses],
            "question_id": [response[5] for response in responses],
            "response_id": [response[6] for response in responses],
            "response_metadata": [response[7] for response in responses],
        }

        return r_data
