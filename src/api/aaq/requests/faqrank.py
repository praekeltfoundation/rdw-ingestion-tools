from pandas import DataFrame, concat


class Faqrank:
    def __init__(self, session):
        self._session = session

    def get_faqranks(self, **kwargs):

        url = "inbounds"

        response_list = self._session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d.keys()} for d in response_list
        ]

        scores_list = []
        for response in response_list:
            id = response["inbound_id"]
            scores = []
            for faq in response["model_scoring"]:
                try:
                    scores.append(
                        {
                            "inbound_id": id,
                            "faq_id": faq,
                            "score": response["model_scoring"][faq][
                                "overall_score"
                            ],
                        }
                    )
                except TypeError:
                    break
            scores_list.append(DataFrame(scores))

        try:
            faq_ranks = concat([DataFrame(d, index=[0]) for d in scores_list])
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                faq_ranks = DataFrame()

        return faq_ranks
