from api.aaq.requests.faqmatches import FAQMatches
from api.aaq.requests.inbounds import Inbounds
from api.aaq.requests.inbounds_ud import InboundsUD
from api.aaq.requests.urgency_rules import UrgencyRules

from . import session


class pyAAQ:
    """A wrapper class for the various Rapidpro endpoints."""

    inbounds = Inbounds(session)
    faqmatches = FAQMatches(session)
    inbounds_ud = InboundsUD(session)
    urgency_rules = UrgencyRules(session)
