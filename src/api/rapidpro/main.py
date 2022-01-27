from api.rapidpro.requests.contacts import Contacts
from api.rapidpro.requests.fields import Fields
from api.rapidpro.requests.flow_starts import FlowStarts
from api.rapidpro.requests.flows import Flows
from api.rapidpro.requests.groups import Groups
from api.rapidpro.requests.runs import Runs

from . import session


class pyRapid:
    """ """

    contacts = Contacts(session)
    fields = Fields(session)
    flow_starts = FlowStarts(session)
    flows = Flows(session)
    groups = Groups(session)
    runs = Runs(session)
