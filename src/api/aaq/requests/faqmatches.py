class FAQMatches:
    def __init__(self, session) -> None:
        self._session = session

    def get_faqmatches(self, **kwargs):

        url = "faqmatches"

        response_list = self._session.get(url, **kwargs)

        return response_list
