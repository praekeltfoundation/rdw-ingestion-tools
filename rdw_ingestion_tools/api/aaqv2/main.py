from attrs import define, field
from httpx import Client

from api.aaqv2.requests.contents import Contents
from api.aaqv2.requests.queries import Queries
from api.aaqv2.requests.urgency_queries import UrgencyQueries
from api.aaqv2.requests.urgency_rules import UrgencyRules

from . import client as default_client


@define
class pyAAQV2:
    """A wrapper class for the various AAQ V2 endpoints.

    The client is configurable so it can be switched out in tests.

    """

    client: Client = field(factory=lambda: default_client)

    contents = field(init=False)
    urgency_rules = field(init=False)
    urgency_queries = field(init=False)
    queries = field(init=False)

    def __attrs_post_init__(self):
        self.contents = Contents(self.client)
        self.urgency_rules = UrgencyRules(self.client)
        self.urgency_queries = UrgencyQueries(self.client)
        self.queries = Queries(self.client)
