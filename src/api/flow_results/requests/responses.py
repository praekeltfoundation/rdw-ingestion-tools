from urllib.parse import urlencode

from attrs import define
from httpx import Client

from .. import get_ids, get_paginated


@define
class Responses:
    """Dedicated to the Responses endpoint of the Flow Results API"""

    client: Client

    def get_responses(
        self,
        start_time: str,
        end_time: str,
        **kwargs: str | int,
    ) -> dict[str, list]:
        """Returns a dict of responses"""

        filters = urlencode(
            {
                "filter[start-timestamp]": start_time,
                "filter[end-timestamp]": end_time,
                **kwargs,
            }
        )

        id_generator = get_ids(self.client)

        responses: dict[str, list] = {
            "flow_id": [],
            "timestamp": [],
            "row_id": [],
            "contact_id": [],
            "session_id": [],
            "question_id": [],
            "response_id": [],
            "response_metadata": [],
        }

        for id in id_generator:
            url = f"{id}/responses/" + "?" + filters

            response_generator = get_paginated(self.client, url=url)

            responses["flow_id"].extend([r[0] for r in response_generator])
            responses["timestamp"].extend([r[1] for r in response_generator])
            responses["row_id"].extend([r[2] for r in response_generator])
            responses["contact_id"].extend([r[3] for r in response_generator])
            responses["session_id"].extend([r[4] for r in response_generator])
            responses["question_id"].extend([r[5] for r in response_generator])
            responses["response_id"].extend([r[6] for r in response_generator])
            responses["response_metadata"].extend(
                [r[7] for r in response_generator]
            )

        return responses
