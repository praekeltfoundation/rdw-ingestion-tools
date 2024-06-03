from api.turn.requests.contacts import Contacts
from api.turn.requests.content import Content
from api.turn.requests.messages import Messages

from . import client


class pyTurn:
    """ """

    messages = Messages(client)
    contacts = Contacts(client)
    content = Content(client)
