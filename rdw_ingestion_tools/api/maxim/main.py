from attrs import define, field
from httpx import Client

from api.maxim.requests.repositories import Repositories
from api.maxim.requests.repositories_logs import RepositoriesLogs

from . import client


@define
class pyMaxim:
    """A wrapper class for the various Maxim respositories endpoints.

    The client is configurable so that it can be switched out in tests.

    """

    client: Client = field(factory=lambda: client)

    repositories: Repositories = field(init=False)
    repositories_logs: RepositoriesLogs = field(init=False)

    def __attrs_post_init__(self):
        self.repositories = Repositories(client=self.client)
        self.repositories_logs = RepositoriesLogs(client=self.client)
