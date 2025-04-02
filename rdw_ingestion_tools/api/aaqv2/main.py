from api.aaq.requests.contents import Contents
from api.aaq.requests.queries import Queries
from api.aaq.requests.urgency_queries import UrgencyQueries
from api.aaq.requests.urgency_rules import UrgencyRules

from . import client


class pyAAQV2:
    """A wrapper class for the various AAQ V2 endpoints."""

    contents = Contents(client)
    urgency_rules = UrgencyRules(client)
    urgency_queries = UrgencyQueries(client)
    queries = Queries(client)
