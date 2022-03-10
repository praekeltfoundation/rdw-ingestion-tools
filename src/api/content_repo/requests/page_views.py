import json

import pandas as pd


class PageViews:
    def __init__(self, session):
        self._session = session

    def get_pageviews(self, ts):

        url = "pageviews/?timestamp_gt=" + ts

        r = self._session.request("GET", url)
        r.raise_for_status()

        r = r.json()

        l = [r]
        while r["next"]:
            r = self._session.request("GET", r["next"]).json()
            l.append(r)

        pageviews = []
        for response in l:
            pageviews.append(pd.json_normalize(response["results"], sep="_"))
        pageviews = pd.concat(pageviews)

        return pageviews
