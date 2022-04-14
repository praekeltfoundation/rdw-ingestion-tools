# Generalised survey endpoints coming.
import json

import pandas as pd


class MQR:
    def __init__(self, session):
        self._session = session

    def get_baseline(self, ts, max_pages=5):
        """
        API only accepts initial timestamp and returns records after.

        """

        url = "mqrbaselinesurvey/?updated_at_gt=" + ts

        r = self._session.request("GET", url)

        r.raise_for_status()
        r = r.json()

        next_page = r["next"]
        l = [r]

        pages = 0
        while next_page and pages < max_pages:
            r = self._session.request("GET", next_page).json()
            next_page = r["next"]
            try:
                l.append(r)
            except NameError:
                l = [r]
            pages += 1

        baseline = []
        for response in l:
            baseline.append(pd.json_normalize(response["results"], sep="_"))
        baseline = pd.concat(baseline)

        return baseline
