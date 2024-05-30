from attrs import define
from httpx import Client

from .. import get_ids


@define
class Flows:
    """Dedicated to the Flows endpoint of the Flow Results API"""

    client: Client

    def get_flows(self, **kwargs: str | int) -> dict[str, dict]:
        """Returns a dict of question and flow data - each returned as a
        nested dict.

        """

        params = {**kwargs}

        id_generator = get_ids(self.client)

        flow_data: dict[str, list] = {
            "id": [],
            "name": [],
            "version": [],
            "created": [],
            "modified": [],
            "title": [],
            "language": [],
        }

        question_data: dict[str, list] = {
            "flow_id": [],
            "id": [],
            "type": [],
            "label": [],
            "type_options": [],
        }

        for id in id_generator:
            url = id
            response = self.client.get(
                url, params=params, follow_redirects=True
            )
            response.raise_for_status()

            attributes = response.json()["data"]["attributes"]

            flow_data["id"].append(response.json()["data"]["id"])
            flow_data["name"].append(attributes["name"])
            flow_data["version"].append(
                attributes["flow-results-specification"]
            )
            flow_data["created"].append(attributes["created"])
            flow_data["modified"].append(attributes["modified"])
            flow_data["title"].append(attributes["title"])
            flow_data["language"].append(
                attributes["resources"][0]["schema"]["language"]
            )

            questions = attributes["resources"][0]["schema"]["questions"]

            for key in list(questions.keys()):
                question_data["flow_id"].append(id)
                question_data["id"].append(key)
                question_data["type"].append(questions[key]["type"])
                question_data["label"].append(questions[key]["label"])
                question_data["type_options"].append(
                    questions[key]["type_options"]
                )

        return {"flows": flow_data, "questions": question_data}
