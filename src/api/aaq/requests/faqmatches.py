import pandas as pd


class FAQMatches:
    def __init__(self, session) -> None:
        self._session = session

    def get_faqmatches(self, **kwargs):

        url = "faqmatches"

        response_list = self._session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d.keys()} for d in response_list
        ]

        faqmatches = pd.concat(
            [pd.DataFrame(d, index=[0]) for d in response_list]
        )

        return faqmatches
