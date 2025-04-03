from collections.abc import Sequence
from typing import Any, Self

from attrs import define
from attrs import fields as dc_fields

JsonObj = dict[str, "Json"]
JsonArr = list["Json"]
Json = str | int | float | bool | JsonObj | JsonArr | None


@define(frozen=True, kw_only=True)
class AAQV2ModelBase:
    """
    Base class for all AAQV2 data types.

    """

    @classmethod
    def from_json(cls, resp_json: JsonObj) -> Self:
        # TODO: Review the specifics of this method.
        names = {f.alias for f in dc_fields(cls)}
        fields = {k: v for k, v in resp_json.items() if k in names}

        # Since we can get arbitrary JSON here, we have to
        # accept ambiguous types.
        return cls(**fields, raw_json=resp_json)  # type: ignore


@define(frozen=True, kw_only=True)
class Content(AAQV2ModelBase):
    """
    AAQV2 Content type that (according to the docs) returns all contents
    for a user.

    This endpoint receives no arguments parameters, so it's unclear whether this
    will return content across *all* users, or simply for the authenticated
    user. For this to function as a data export API, we'd need to have data
    for all users.

    """

    content_title: str
    content_text: str
    content_tags: list
    content_metadata: dict
    is_archived: bool
    content_id: int
    user_id: int
    created_datetime_utc: str
    updated_datetime_utc: str
    positive_votes: int
    negative_votes: int


@define(frozen=True, kw_only=True)
class UrgencyRule(AAQV2ModelBase):
    """
    AAQV2 Urgency Rule type that (according to the docs) returns all
    urgency rules for a user.

    This endpoint receives no arguments parameters, so it's unclear whether this
    will return rules across *all* users, or simply for the authenticated user.
    For this to function as a data export API, we'd need to have data for
    all users.

    """

    created_datetime_utc: str
    updated_datetime_utc: str
    urgency_rule_id: int
    urgency_rule_metadata: dict
    urgency_rule_text: str
    user_id: int


@define(frozen=True, kw_only=True)
class QueryResponse(AAQV2ModelBase):
    """
    A subtype in the Query type.

    """

    response_id: int
    # Figure out what type this is
    search_results: Any
    llm_response: str | None
    response_datetime_utc: str


@define(frozen=True, kw_only=True)
class ResponseFeedback(AAQV2ModelBase):
    """
    A subtype in the Query type.

    """

    feedback_id: int
    feedback_sentiment: str
    feedback_text: str | None
    feedback_datetime_utc: str


@define(frozen=True, kw_only=True)
class Query(AAQV2ModelBase):
    """
    AAQV2 Query type that (according to the docs) returns all queries for a user
    between a start and an end date.

    "Get all queries including child records for a user between a start
    and end date."

    Note that the start_date and end_date can be provided as a date
    or datetime object.

    """

    query_id: int
    user_id: int
    query_text: str
    query_metadata: Any
    query_datetime_utc: str
    response: Sequence[QueryResponse]
    response_feedback: Sequence[ResponseFeedback]
    # Similar to the above except content feedback also has a content id.
    # Just need to account for this.
    content_feedback: Sequence[ResponseFeedback]


@define(frozen=True, kw_only=True)
class UrgencyQueryResponseExtract(AAQV2ModelBase):
    """
    A subtype in the UrgencyQuery type.

    """

    urgency_response_id: int
    is_urgent: bool
    matched_rules: Sequence[str | None]
    details: Any
    response_datetime_utc: str


@define(frozen=True, kw_only=True)
class UrgencyQuery(AAQV2ModelBase):
    """
    AAQV2 UrgencyQuery type that allows you to, according to the docs, to:

    "Get all urgency queries including child records for a user between a start
    and end date."

    Note that the start_date and end_date can be provided as a date
    or datetime object.

    """

    urgency_query_id: int
    user_id: int
    message_text: str
    message_datetime_utc: str
    response: UrgencyQueryResponseExtract | None
