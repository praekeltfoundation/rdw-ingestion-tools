import json
from functools import cached_property

from attrs import define, field
from httpx import Client, WSGITransport
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response

from .models import Content, Query, UrgencyQuery, UrgencyRule


@define
class AAQHTTPErr(Exception):
    status_code: int
    error: str
    message: str


def mk_422(message: str) -> AAQHTTPErr:
    return AAQHTTPErr(status_code=422, error="Unprocessable Entity", message=message)


@define
class FakeAAQV2:
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

    def _json_response(self, data: object, status: int = 200) -> Response:
        return Response(
            json.dumps(data, default=self._serialize),
            status=status,
            content_type="application/json",
        )

    def _serialize(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        elif hasattr(obj, "__attrs_attrs__"):
            return {a.name: getattr(obj, a.name) for a in obj.__attrs_attrs__}
        return str(obj)

    def _err_handler(self, e: AAQHTTPErr) -> Response:
        return self._json_response(
            {"statusCode": e.status_code, "error": e.error, "message": e.message},
            status=e.status_code,
        )

    def dispatch_request(self, request: Request) -> Response:
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, _ = adapter.match()
            return endpoint()
        except AAQHTTPErr as e:
            return self._err_handler(e)
        except HTTPException as e:
            return e.get_response(request.environ)

    @cached_property
    def url_map(self) -> Map:
        return Map(
            [
                Rule("/queries", endpoint=self._handle_queries),
                Rule("/urgency_queries", endpoint=self._handle_urgency_queries),
                Rule("/contents", endpoint=self._handle_contents),
                Rule("/urgency_rules", endpoint=self._handle_urgency_rules),
            ]
        )

    def _handle_queries(self):
        return self._json_response(self.queries)

    def _handle_urgency_queries(self):
        return self._json_response(self.urgency_queries)

    def _handle_contents(self):
        return self._json_response(self.contents)

    def _handle_urgency_rules(self):
        return self._json_response(self.urgency_rules)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def client(self) -> Client:
        return Client(
            base_url="http://fake_aaqv2",
            transport=WSGITransport(self.wsgi_app),
        )
