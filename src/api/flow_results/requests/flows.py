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

        flows: dict[str, list] = {
            "id": [],
            "name": [],
            "version": [],
            "created": [],
            "modified": [],
            "title": [],
            "language": [],
        }

        questions: dict[str, list] = {
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

            _attrs = response.json()["data"]["attributes"]

            flows["id"].append(response.json()["data"]["id"])
            flows["name"].append(_attrs["name"])
            flows["version"].append(_attrs["flow-results-specification"])
            flows["created"].append(_attrs["created"])
            flows["modified"].append(_attrs["modified"])
            flows["title"].append(_attrs["title"])
            flows["language"].append(
                _attrs["resources"][0]["schema"]["language"]
            )

            questions_response = _attrs["resources"][0]["schema"]["questions"]

            for key in list(questions_response.keys()):
                questions["flow_id"].append(id)
                questions["id"].append(key)
                questions["type"].append(questions_response[key]["type"])
                questions["label"].append(questions_response[key]["label"])
                questions["type_options"].append(
                    questions_response[key]["type_options"]
                )

        return {"flows": flows, "questions": questions}
