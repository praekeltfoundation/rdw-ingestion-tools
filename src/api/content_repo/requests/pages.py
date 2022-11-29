from pandas import concat, json_normalize


class Pages:
    def __init__(self, session):
        self._session = session

    def get_pages(self, page=None):
        """
        Returns content pages.

        """

        url = "pages"

        if not page:
            response = self._session.request("GET", url)
            response.raise_for_status()
            response = response.json()
            next_page = response["next"]
            response_list = [response]
        else:
            next_page = page

        while next_page:
            print("Retrieving pages for page: ", next_page)
            response = self._session.request("GET", next_page).json()
            next_page = response["next"]
            try:
                response_list.append(response)
            except NameError:
                response_list = [response]

        pages = []
        for item in response_list:
            pages.append(json_normalize(item["results"], sep="_"))
        pages = concat(pages)

        return {"pages": pages}
