from pandas import DataFrame, concat


class Inbounds:
    def __init__(self, session):
        self._session = session

    def get_inbounds(self, **kwargs):

        url = "inbounds"

        response_list = self._session.get(url, **kwargs)

        response_list = [
            {key: str(d[key]) for key in d.keys()} for d in response_list
        ]

        try:
            inbounds = concat([DataFrame(d, index=[0]) for d in response_list])
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                inbounds = DataFrame()

        return inbounds

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
            for faq in eval(response["model_scoring"]):
                faqs = eval(response["model_scoring"])[faq]
                if isinstance(faqs, str):
                    break
                rank = ""
                if "rank" in faqs.keys():
                    rank = faqs["rank"]
                scores.append(
                    {
                        "inbound_id": id,
                        "faq_id": faq,
                        "score": faqs["overall_score"],
                        "rank": rank,
                    }
                )
            scores_list.append(DataFrame(scores))

        try:
            faq_ranks = concat([DataFrame(d, index=[0]) for d in scores_list])
        except ValueError as e:
            if str(e) != "No objects to concatenate":
                raise
            else:
                faq_ranks = DataFrame()

        return faq_ranks
