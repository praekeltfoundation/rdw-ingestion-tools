from attrs import define
from httpx import Client
from polars import LazyFrame

from ..extensions.httpx import get
from ..schemas.contents import contents_schema


@define
class Contents:
    """Dedicated to the contents endpoint of the AAQ V2 Data Export API."""

    client: Client

    def get_contents(self, **kwargs: str | int) -> LazyFrame:
        """Get a pandas DataFrame of contents.

        No time-based query parameters are supported for this endpoint.
        Should return the full contents object or an empty DataFrame if
        no records are returned by the API.

        """

        url = "contents"

        contents_generator = get(self.client, url, **kwargs)

        return LazyFrame(contents_generator, schema=contents_schema)
