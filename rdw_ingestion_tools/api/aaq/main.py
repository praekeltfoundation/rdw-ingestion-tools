from attrs import define, field
from httpx import Client

from api.aaq.requests.faqmatches import FAQMatches
from api.aaq.requests.inbounds import Inbounds
from api.aaq.requests.inbounds_ud import InboundsUD
from api.aaq.requests.urgency_rules import UrgencyRules

from . import client as default_client


@define
class pyAAQ:
    """A wrapper class for the various AAQ endpoints.

    The client is configurable so it can be switched out in tests.

    """

    client: Client = field(factory=lambda: default_client)

    inbounds = field(init=False)
    faqmatches = field(init=False)
    inbounds_ud = field(init=False)
    urgency_rules = field(init=False)

    def __attrs_post_init__(self):
        self.inbounds = Inbounds(self.client)
        self.faqmatches = FAQMatches(self.client)
        self.inbounds_ud = InboundsUD(self.client)
        self.urgency_rules = UrgencyRules(self.client)
