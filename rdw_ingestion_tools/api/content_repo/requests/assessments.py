from attrs import define
from httpx import Client
from pandas import DataFrame

from api import concatenate

from ..extensions.httpx import get_paginated


@define
class Assessments:
    """Dedicated to the Assessments endpoint of the Content Repo API"""

    client: Client

    def get_assessments(self, max_pages: int = 5) -> DataFrame:
        """Get a pandas DataFrame of Content Repo assessments.

        No time-based query parameters are supported by the endpoint.
        Full set of assessments accessible via pagination.

        """

        url = "assessments"

        assessments_generator = get_paginated(
            client=self.client,
            url=url,
            max_pages=max_pages,
        )

        assessments = concatenate(assessments_generator)

        return assessments
