from api.turn.requests.contacts import Contacts
from api.turn.requests.content import Content
from api.turn.requests.messages import Messages

from . import session


class pyTurn:
    """ """

    messages = Messages(session)
    contacts = Contacts(session)
    content = Content(session)
