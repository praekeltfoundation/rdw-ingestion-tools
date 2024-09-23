from api.rapidpro.requests.contacts import Contacts
from api.rapidpro.requests.fields import Fields
from api.rapidpro.requests.flow_starts import FlowStarts
from api.rapidpro.requests.flows import Flows
from api.rapidpro.requests.groups import Groups
from api.rapidpro.requests.runs import Runs

from . import client


class pyRapid:
    """A wrapper class for the various Rapidpro endpoints."""

    contacts = Contacts(client)
    fields = Fields(client)
    flow_starts = FlowStarts(client)
    flows = Flows(client)
    groups = Groups(client)
    runs = Runs(client)
