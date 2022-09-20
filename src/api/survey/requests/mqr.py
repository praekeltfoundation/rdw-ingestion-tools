import pandas as pd


class MQR:
    def __init__(self, session):
        self._session = session

    def get_baseline(self, ts, max_pages=5):
        """
        API only accepts initial timestamp and returns records after.

        """

        url = "mqrbaselinesurvey/?updated_at_gt=" + ts

        response = self._session.request("GET", url)

        response.raise_for_status()
        response = response.json()

        next_page = response["next"]
        response_list = [response]

        pages = 0
        while next_page and pages < max_pages:
            response = self._session.request("GET", next_page).json()
            next_page = response["next"]
            try:
                response_list.append(response)
            except NameError:
                response_list = [response]
            pages += 1

        baseline = []
        for item in response_list:
            baseline.append(pd.json_normalize(item["results"], sep="_"))
        baseline = pd.concat(baseline)

        return baseline
