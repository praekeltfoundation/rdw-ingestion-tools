from api.flow_results.requests.flows import Flows
from api.flow_results.requests.responses import Responses

from . import client


class pyFlows:
    """A wrapper class for the various Flow Results endpoints."""

    flows = Flows(client)
    responses = Responses(client)
