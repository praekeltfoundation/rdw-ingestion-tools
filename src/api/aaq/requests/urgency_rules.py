from pandas import DataFrame, concat


class UrgencyRules:
    def __init__(self, session) -> None:
        self._session = session

    def get_urgency_rules(self, **kwargs):
        url = "urgency_rules"

        response_list = self._session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d} for d in response_list
        ]

        try:
            urgency_rules = concat(
                [DataFrame(d, index=[0]) for d in response_list]
            )
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                urgency_rules = DataFrame()

        return urgency_rules
