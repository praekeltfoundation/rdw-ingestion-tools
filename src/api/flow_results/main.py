from api.flow_results.requests.flows import Flows
from api.flow_results.requests.responses import Responses

from . import session


class pyFlows:
    """ """

    flows = Flows(session)
    responses = Responses(session)
