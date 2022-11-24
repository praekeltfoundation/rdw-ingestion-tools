class UrgencyRules:
    def __init__(self, session) -> None:
        self._session = session

    def get_urgency_rules(self, **kwargs):

        url = "urgency_rules"

        response_list = self._session.get(url, **kwargs)

        return response_list
