from attrs import define, field
from httpx import Client

from api.turn_bq.requests.cards import Cards
from api.turn_bq.requests.chats import Chats
from api.turn_bq.requests.contacts import Contacts
from api.turn_bq.requests.flow_results import FlowResults
from api.turn_bq.requests.flow_results_data_packages import (
    FlowResultsDataPackages,
)
from api.turn_bq.requests.messages import Messages
from api.turn_bq.requests.statuses import Statuses

from .client import get_client


@define
class pyTurnBQ:
    """A wrapper class for the various Turn BQ endpoints.

    The client is configurable so that it can be switched out in tests.

    """

    client: Client = field(factory=get_client)

    cards: Cards = field(init=False)
    contacts: Contacts = field(init=False)
    chats: Chats = field(init=False)
    messages: Messages = field(init=False)
    flow_results_data_packages: FlowResultsDataPackages = field(init=False)
    flow_results: FlowResults = field(init=False)
    statuses: Statuses = field(init=False)

    def __attrs_post_init__(self):
        self.cards = Cards(client=self.client)
        self.contacts = Contacts(client=self.client)
        self.chats = Chats(client=self.client)
        self.messages = Messages(client=self.client)
        self.flow_results_data_packages = FlowResultsDataPackages(client=self.client)
        self.flow_results = FlowResults(client=self.client)
        self.statuses = Statuses(client=self.client)
