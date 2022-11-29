from api.aaq.requests.faqmatches import FAQMatches
from api.aaq.requests.inbounds import Inbounds

from . import session


class pyAAQ:
    """ """

    inbounds = Inbounds(session)
    faqmatches = FAQMatches(session)
