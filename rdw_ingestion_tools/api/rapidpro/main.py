from attrs import define, field
from httpx import Client

from api.rapidpro.requests.contacts import Contacts
from api.rapidpro.requests.fields import Fields
from api.rapidpro.requests.flow_starts import FlowStarts
from api.rapidpro.requests.flows import Flows
from api.rapidpro.requests.groups import Groups
from api.rapidpro.requests.runs import Runs

from . import client as default_client


@define
class pyRapid:
    """A wrapper class for the various Rapidpro endpoints.

    The client is configurable so that it can be switched out in tests.

    """

    client: Client = field(factory=lambda: default_client)

    contacts = field(init=False)
    fields = field(init=False)
    flow_starts = field(init=False)
    flows = field(init=False)
    groups = field(init=False)
    runs = field(init=False)

    def __attrs_post_init__(self):
        self.contacts = Contacts(client=self.client)
        self.fields = Fields(client=self.client)
        self.flow_starts = FlowStarts(client=self.client)
        self.flows = Flows(client=self.client)
        self.groups = Groups(client=self.client)
        self.runs = Runs(client=self.client)
