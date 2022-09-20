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
            response = self._session.request("GET", url)
            response.raise_for_status()
            response = response.json()
            next_page = response["next"]
            response_list = [response]
        else:
            next_page = page

        pages = 0
        while next_page and pages < max_pages:
            response = self._session.request("GET", next_page).json()
            next_page = response["next"]
            try:
                response_list.append(response)
            except NameError:
                response_list = [response]
            pages += 1

        pageviews = []
        for item in response_list:
            pageviews.append(pd.json_normalize(item["results"], sep="_"))
        pageviews = pd.concat(pageviews)

        if response["next"]:
            page = response["next"]
        else:
            page = None

        return {"pageviews": pageviews, "page": page}
