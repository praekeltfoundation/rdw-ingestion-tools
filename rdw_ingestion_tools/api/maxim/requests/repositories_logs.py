from attrs import define
from httpx import Client
from polars import LazyFrame

from .. import config_from_env
from ..extensions.httpx import get, post

WORKSPACE_ID = config_from_env("WORKSPACE_ID")


@define
class RepositoriesLogs:
    """Dedicated to the repositories endpoint of the Maxim logs API."""

    client: Client

    def get_repositories_logs(
        self, start_date: str, end_date: str, type: str
    ) -> LazyFrame:
        """Get a polars LazyFrame of repositories logs."""

        logs_url = "log-repositories/logs/search"

        # Get all repository IDs
        id_url = "log-repositories"
        repositories_id_generator = get(self.client, url=id_url, field="id")

        # Populate request data
        data = {
            "workspaceId": WORKSPACE_ID,
            "timestamp": {"gte": start_date, "lte": end_date},
            "sessionId": "",
            "searchQuery": "",
            "page": 0,
            "limit": 1,
            "type": type,
        }

        # Retrieve logs for all repository IDs
        for repository in repositories_id_generator:
            data["id"] = repository["id"]
            log_repositories_generator = post(self.client, logs_url, data)

        return LazyFrame(log_repositories_generator)
    
