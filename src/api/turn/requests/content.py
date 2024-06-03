from attrs import define
from httpx import Client
from pandas import DataFrame, json_normalize


@define
class Content:
    """Dedicated to the content export endpoint of the Turn Data Export API."""

    client: Client

    def get_content(self, **kwargs: str | int) -> DataFrame:
        """Get a pandas DataFrame of content.

        No time-based query parameters are supported by this endpoint.

        pyTurn.content.get_content()

        See examples/turn/content.py

        """
        url = "export"

        params = {**kwargs}

        content_response = self.client.get(url=url, params=params)
        content_response.raise_for_status()

        content = json_normalize(content_response.json()["data"])

        return content
