from attrs import define, field
from httpx import Client

from api.flow_results.requests.flows import Flows
from api.flow_results.requests.responses import Responses

from . import client as default_client


@define
class pyFlows:
    """A wrapper class for the various Flow Results endpoints.

    The client is configurable so it can be switched out in tests.

    """

    client: Client = field(factory=lambda: default_client)

    flows: Flows = field(init=False)
    responses: Responses = field(init=False)

    def __attrs_post_init__(self):
        self.flows = Flows(client=self.client)
        self.responses = Responses(client=self.client)
