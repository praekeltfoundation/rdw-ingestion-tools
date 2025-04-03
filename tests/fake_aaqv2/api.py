from functools import cached_property

from attrs import define, field
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .models import Content, Query, UrgencyQuery, UrgencyRule


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
    return AAQHTTPErr(status_code=422, error="Unprocessable Entity", message=message)


# The AAQV2 data export API doesn't support pagination.
@define
class FakeAAQV2:
    """
    A fake implementation of the AAQV2 data export API endpoints.
    """

    urgency_rules: list[UrgencyRule] = field(factory=list)
    urgency_queries: list[UrgencyQuery] = field(factory=list)
    queries: list[Query] = field(factory=list)
    contents: list[Content] = field(factory=list)

    def add_urgency_rules(self, *urgency_rules: UrgencyRule) -> None:
        self.urgency_rules.extend(urgency_rules)

    def add_urgency_queries(self, *urgency_queries: UrgencyQuery) -> None:
        self.urgency_queries.extend(urgency_queries)

    def add_contents(self, *contents: Content) -> None:
        self.contents.extend(contents)

    def add_queries(self, *queries: Query) -> None:
        self.queries.extend(queries)

    async def get_queries(self, request: Request) -> JSONResponse:
        # TODO: Logic to validate start and end dates and filter output.
        return JSONResponse(self.queries)

    async def get_urgency_queries(self, request: Request) -> JSONResponse:
        # TODO: Logic to validate start and end dates and filter output.
        return JSONResponse(self.urgency_queries)

    async def get_contents(self) -> JSONResponse:
        # Do we need a request arg?
        return JSONResponse(self.contents)

    async def get_urgency_rules(self) -> JSONResponse:
        # Do we need a request arg?
        return JSONResponse(self.urgency_rules)

    def _err_handler(self, _req: Request, e: Exception) -> JSONResponse:
        assert isinstance(e, AAQHTTPErr)
        return JSONResponse(
            {"statusCode": e.status_code, "error": e.error, "message": e.message},
            status_code=422,
        )

    @property
    def _routes(self) -> list[Route]:
        return [
            Route("/data-api/queries", self.get_queries),
            Route("/data-api/urgency_queries", self.get_urgency_queries),
            Route("/data-api/contents", self.get_contents),
            Route("/data-api/urgency_rules", self.get_urgency_rules),
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
