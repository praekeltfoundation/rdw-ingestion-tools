from typing import Sequence, Any

from functools import cached_property

from attrs import define, fields
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from abc import ABCMeta

from models import Content, UrgencyRule, UrgencyQuery, Query


@define
class AAQHTTPErr(Exception):
    """
    Starlette's HTTPException doesn't include 422 validation errors.

    The only error the data export API endpoints surface are
    validation errors where datetime parameters are incorrect.

    """

    status_code: int
    error: str
    message: str

    def mk_422(message: str) -> AAQHTTPErr:
        return APHTTPErr(
            status_code=422, error="Unprocessable Entity", message=message
        )


# The AAQV2 data export API doesn't support pagination.
@define
class FakeAAQV2:
    """
    A fake implementation of the AAQV2 data export API endpoints.
    """

    urgency_rules: Sequence[UrgencyRule]
    urgency_queries: Sequence[UrgencyQuery]
    queries: Sequence[Query]
    contents: Sequence[Content]

    def add_urgency_rules(self, *urgency_rules: UrgencyRule) -> None:
        self.urgency_rules.extend(urgency_rules)

    def add_urgency_queries(self, *urgency_queries: UrgencyQuery) -> None:
        self.urgency_queries.extend(urgency_queries)

    def add_contents(self, *contents: Content) -> None:
        self.contents.extend(contents)

    def add_queries(self, *queries: Query) -> None:
        self.queries.extend(queries)

    async def queries(self, request: Request) -> JSONResponse:
        # TODO: Logic to validate start and end dates and filter output.
        return JSONResponse(self.queries)

    async def urgency_queries(self, request: Request) -> JSONResponse:
        # TODO: Logic to validate start and end dates and filter output.
        return JSONResponse(self.urgency_queries)

    async def contents(self) -> JSONReponse:
        # Do we need a request arg?
        return JSONResponse(self.contents)

    async def urgency_rules(self) -> JSONResponse:
        # Do we need a request arg?
        return JSONResponse(self.urgency_rules)

    @property
    def _routes(self) -> list[Route]:
        return [
            Route("/data-api/queries", self.queries),
            Route("/data-api/urgency_queries", self.urgency_queries),
            Route("/data-api/contents", self.contents),
            Route("/data-api/urgency_rules", self.urgency_rules),
        ]

    @cached_property
    def app(self) -> Starlette:
        return Starlette(
            routes=self._routes,
            exception_handlers={AAQHTTPErr: self._err_handler},
        )

    def async_client(self) -> AsyncClient:
        return AsyncClient(
            base_url="https://fake_aaqv2/api",
            transport=ASGITransport(app=self.app),
        )
