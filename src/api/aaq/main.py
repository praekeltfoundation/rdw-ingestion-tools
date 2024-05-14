from api.aaq.requests.faqmatches import FAQMatches
from api.aaq.requests.inbounds import Inbounds
from api.aaq.requests.inbounds_ud import InboundsUD
from api.aaq.requests.urgency_rules import UrgencyRules

from . import base_session


class pyAAQ:
    """A wrapper class for the various AAQ endpoints."""

    inbounds = Inbounds(base_session)
    faqmatches = FAQMatches(base_session)
    inbounds_ud = InboundsUD(base_session)
    urgency_rules = UrgencyRules(base_session)
