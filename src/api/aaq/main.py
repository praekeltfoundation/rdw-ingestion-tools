from api.aaq.requests.faqmatches import FAQMatches
from api.aaq.requests.inbounds import Inbounds
from api.aaq.requests.inbounds_ud import InboundsUD
from api.aaq.requests.urgency_rules import UrgencyRules

from . import client


class pyAAQ:
    """A wrapper class for the various AAQ endpoints."""

    inbounds = Inbounds(client)
    faqmatches = FAQMatches(client)
    inbounds_ud = InboundsUD(client)
    urgency_rules = UrgencyRules(client)
