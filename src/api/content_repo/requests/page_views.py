import pandas as pd


class PageViews:
    def __init__(self, session):
        self._session = session

    def get_pageviews(self, ts, max_pages=5, page=None):
        """
        API only accepts initial timestamp and returns records after.

        """

        url = "pageviews/?timestamp_gt=" + ts

        if not page:
            r = self._session.request("GET", url)
            r.raise_for_status()
            r = r.json()
            next_page = r["next"]
            response_list = [r]
        else:
            next_page = page

        pages = 0
        while next_page and pages < max_pages:
            r = self._session.request("GET", next_page).json()
            next_page = r["next"]
            try:
                response_list.append(r)
            except NameError:
                response_list = [r]
            pages += 1

        pageviews = []
        for response in response_list:
            pageviews.append(pd.json_normalize(response["results"], sep="_"))
        pageviews = pd.concat(pageviews)

        if r["next"]:
            page = r["next"]
        else:
            page = None

        return {"pageviews": pageviews, "page": page}
