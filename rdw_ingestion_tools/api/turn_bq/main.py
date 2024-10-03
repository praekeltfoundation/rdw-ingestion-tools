from api.turn_bq.requests.cards import Cards
from api.turn_bq.requests.chats import Chats
from api.turn_bq.requests.contacts import Contacts
from api.turn_bq.requests.flow_results import FlowResults
from api.turn_bq.requests.flow_results_data_packages import (
    FlowResultsDataPackages,
)
from api.turn_bq.requests.messages import Messages
from api.turn_bq.requests.statuses import Statuses

from . import client


class pyTurnBQ:
    """ """

    cards = Cards(client)
    contacts = Contacts(client)
    chats = Chats(client)
    messages = Messages(client)
    flow_results_data_packages = FlowResultsDataPackages(client)
    flow_results = FlowResults(client)
    statuses = Statuses(client)
