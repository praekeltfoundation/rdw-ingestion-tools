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
            return endpoint(request)
        except AAQHTTPErr as e:
            return self._err_handler(e)
        except HTTPException as e:
            return e.get_response(request.environ)

    @cached_property
    def url_map(self) -> Map:
        return Map(
            [
                Rule("/queries", endpoint=self._handle_queries),
                Rule("/urgency-queries", endpoint=self._handle_urgency_queries),
                Rule("/contents", endpoint=self._handle_contents),
                Rule("/urgency-rules", endpoint=self._handle_urgency_rules),
            ]
        )

    def _handle_queries(self, request: Request):
        start = request.args.get("start_date")
        end = request.args.get("end_date")

        return self._json_response(
            [
                query
                for query in self.queries
                if query.query_datetime_utc >= start and query.query_datetime_utc <= end
            ]
        )

    def _handle_urgency_queries(self, request: Request):
        start = request.args.get("start_date")
        end = request.args.get("end_date")

        return self._json_response(
            [
                urgency_query
                for urgency_query in self.urgency_queries
                if urgency_query.message_datetime_utc >= start
                and urgency_query.message_datetime_utc <= end
            ]
        )

    def _handle_contents(self, request: Request):
        return self._json_response(self.contents)

    def _handle_urgency_rules(self, request: Request):
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
