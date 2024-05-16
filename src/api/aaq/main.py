from api.aaq.requests.faqmatches import FAQMatches
from api.aaq.requests.inbounds import Inbounds
from api.aaq.requests.inbounds_ud import InboundsUD
from api.aaq.requests.urgency_rules import UrgencyRules

from . import httpx_client


class pyAAQ:
    """A wrapper class for the various AAQ endpoints."""

    inbounds = Inbounds(httpx_client)
    faqmatches = FAQMatches(httpx_client)
    inbounds_ud = InboundsUD(httpx_client)
    urgency_rules = UrgencyRules(httpx_client)

    def httpx_close():
        """Exposing the ability to close the client here.

        The client is being used outside of a context manager
        and httpx recommends closing these connections in this case.

        """
        httpx_client.close()
