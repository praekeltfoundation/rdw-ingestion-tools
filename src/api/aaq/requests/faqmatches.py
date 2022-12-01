from pandas import DataFrame, concat


class FAQMatches:
    def __init__(self, session) -> None:
        self._session = session

    def get_faqmatches(self, **kwargs):

        url = "faqmatches"

        response_list = self._session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d.keys()} for d in response_list
        ]

        try:
            faqmatches = concat(
                [DataFrame(d, index=[0]) for d in response_list]
            )
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                faqmatches = DataFrame()

        return faqmatches
