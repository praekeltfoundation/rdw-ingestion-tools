from api.aaq.requests.faqmatches import FAQMatches
from api.aaq.requests.inbounds import Inbounds
from api.aaq.requests.inbounds_ud import InboundsUD
from api.aaq.requests.urgency_rules import UrgencyRules

from . import base_client


class pyAAQ:
    """A wrapper class for the various AAQ endpoints."""

    inbounds = Inbounds(base_client)
    faqmatches = FAQMatches(base_client)
    inbounds_ud = InboundsUD(base_client)
    urgency_rules = UrgencyRules(base_client)
