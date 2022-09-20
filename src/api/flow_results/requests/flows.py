class Flows:
    def __init__(self, session):
        self._session = session

    def get_ids(self, **kwargs):

        params = {**kwargs}

        request = ""

        response = self._session.get(request, params=params)
        response.raise_for_status()

        ids = [flow["id"] for flow in response.json()["data"]]

        return ids

    def get(self, **kwargs):

        ids = self.get_ids()

        params = {**kwargs}

        flows = []
        for id in ids:
            request = id
            response = self._session.get(request, params=params)
            if response.ok:
                flows.append(response.json())
            else:
                pass

        f_data = {
            "id": [],
            "name": [],
            "version": [],
            "created": [],
            "modified": [],
            "title": [],
            "language": [],
        }

        for flow in flows:
            f_data["id"].append(flow["data"]["id"])
            f_data["name"].append(flow["data"]["attributes"]["name"])
            f_data["version"].append(
                flow["data"]["attributes"]["flow-results-specification"]
            )
            f_data["created"].append(flow["data"]["attributes"]["created"])
            f_data["modified"].append(flow["data"]["attributes"]["modified"])
            f_data["title"].append(flow["data"]["attributes"]["title"])
            f_data["language"].append(
                flow["data"]["attributes"]["resources"][0]["schema"][
                    "language"
                ]
            )

        q_data = {
            "flow_id": [],
            "id": [],
            "type": [],
            "label": [],
            "type_options": [],
        }

        questions = [
            flow["data"]["attributes"]["resources"][0]["schema"]["questions"]
            for flow in flows
        ]

        for question, flow_id in zip(questions, ids):
            id = flow_id
            for key in list(question.keys()):
                q_data["flow_id"].append(id)
                q_data["id"].append(key)
                q_data["type"].append(question[key]["type"])
                q_data["label"].append(question[key]["label"])
                q_data["type_options"].append(question[key]["type_options"])

        return {"flows": f_data, "questions": q_data}
