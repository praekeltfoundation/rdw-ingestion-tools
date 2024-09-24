from api.turn_bq.requests.cards import Cards
from api.turn_bq.requests.chats import Chats
from api.turn_bq.requests.contacts import Contacts

from . import client


class pyTurnBQ:
    """ """

    cards = Cards(client)
    contacts = Contacts(client)
    chats = Chats(client)
