import typing

import pytest
from polars import LazyFrame
from polars.exceptions import SchemaError
from polars.testing import assert_frame_equal

from rdw_ingestion_tools.api.aaqv2 import pyAAQV2
from rdw_ingestion_tools.api.aaqv2.schemas.contents import contents_schema
from rdw_ingestion_tools.api.aaqv2.schemas.queries import queries_schema
from rdw_ingestion_tools.api.aaqv2.schemas.urgency_queries import urgency_queries_schema
from rdw_ingestion_tools.api.aaqv2.schemas.urgency_rules import urgency_rules_schema
from tests.test_aaqv2.fake_aaqv2.api import FakeAAQV2
from tests.test_aaqv2.fake_aaqv2.models import (
    Content,
    ContentFeedback,
    Query,
    QueryResponse,
    ResponseFeedback,
    SearchResults,
    UrgencyQuery,
    UrgencyQueryResponseDetails,
    UrgencyQueryResponseExtract,
    UrgencyRule,
)


@pytest.fixture
def fake_aaqv2() -> FakeAAQV2:
    return FakeAAQV2()


@pytest.fixture
def aaqv2(fake_aaqv2) -> pyAAQV2:
    return pyAAQV2(client=fake_aaqv2.client())


def test_get_contents_single_record(fake_aaqv2, aaqv2):
    """
    When get is called against the contents endpoint a correct dataframe of
    contents is returned.

    """
    content = Content(
        content_title="content",
        content_text="this is content",
        content_tags=["this", "is", "content"],
        content_metadata={},
        is_archived=False,
        content_id=1,
        display_number=0,
        created_datetime_utc="2020-01-01T00:00:00",
        negative_votes=100,
        positive_votes=0,
        updated_datetime_utc="2020-01-01T00:00:00",
        workspace_id=0,
    )

    fake_aaqv2.add_contents(content)

    contents = aaqv2.contents.get_contents()

    assert_frame_equal(contents, LazyFrame([content.to_dict()]))


def test_get_urgency_rules_single_record(fake_aaqv2, aaqv2):
    """
    When get is called against the urgency rules endpoint a correct dataframe of
    urgency rules is returned.

    """
    urgency_rule = UrgencyRule(
        urgency_rule_metadata={},
        urgency_rule_text="S.O.S.",
        created_datetime_utc="2020-01-01T00:00:00",
        updated_datetime_utc="2020-01-01T00:00:00",
        urgency_rule_id=1,
        workspace_id=0,
    )

    fake_aaqv2.add_urgency_rules(urgency_rule)

    urgency_rules = aaqv2.urgency_rules.get_urgency_rules()

    assert_frame_equal(urgency_rules, LazyFrame([urgency_rule.to_dict()]))


def test_get_queries_single_record_in_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the queries endpoint a correct dataframe of
    queries is returned with records inside the specified timeframe.

    """
    search_results = SearchResults(title="Title", text="text", id=0, distance=0.05)
    query_response = QueryResponse(
        llm_response="response",
        response_datetime_utc="2020-01-01T00:00:00",
        response_id=1,
        search_results={
            "0": search_results,
            "1": search_results,
            "2": search_results,
            "3": search_results,
        },
    )

    response_feedback = ResponseFeedback(
        feedback_datetime_utc="2020-01-01T00:00:00",
        feedback_id=1,
        feedback_sentiment="Bad",
        feedback_text="Bad",
    )

    content_feedback = ContentFeedback(
        content_id=1,
        feedback_datetime_utc="2020-01-01T00:00:00",
        feedback_id=1,
        feedback_sentiment="Bad",
        feedback_text="Bad",
    )

    query = Query(
        content_feedback=[content_feedback],
        query_datetime_utc="2020-01-01T01:00:00",
        query_id=1,
        query_metadata={},
        query_text="This is my query.",
        response=[query_response],
        response_feedback=[response_feedback],
        workspace_id=0,
    )

    fake_aaqv2.add_queries(query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    queries = aaqv2.queries.get_queries(start_date=start_date, end_date=end_date)

    assert_frame_equal(queries, LazyFrame([query.to_dict()]))


def test_get_queries_single_record_outside_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the queries endpoint, and no records exist within
    the requested timeframe, an empty DataFrame is returned.

    """
    search_results = SearchResults(title="Title", text="text", id=0, distance=0.05)

    query_response = QueryResponse(
        response_id=1,
        search_results={
            "0": search_results,
            "1": search_results,
            "2": search_results,
            "3": search_results,
        },
        llm_response="response",
        response_datetime_utc="2020-01-01T00:00:00",
    )

    response_feedback = ResponseFeedback(
        feedback_id=1,
        feedback_sentiment="Bad",
        feedback_text=None,
        feedback_datetime_utc="2020-01-01T00:00:00",
    )

    content_feedback = ContentFeedback(
        feedback_id=1,
        feedback_sentiment="Bad",
        feedback_text="Bad",
        feedback_datetime_utc="2020-01-01T00:00:00",
        content_id=1,
    )

    query = Query(
        query_id=1,
        query_text="This is my query.",
        query_metadata="Some metadata",
        query_datetime_utc="2020-01-01T00:00:00",
        response=[query_response],
        response_feedback=[response_feedback],
        content_feedback=[content_feedback],
        workspace_id=0,
    )

    fake_aaqv2.add_queries(query)

    start_date = "2020-01-01T01:00:00"
    end_date = "2020-01-02T00:00:00"
    queries = aaqv2.queries.get_queries(start_date=start_date, end_date=end_date)

    assert queries.collect().is_empty()


def test_get_urgency_queries_single_record_in_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the urgency queries endpoint a correct dataframe of
    urgency queries is returned with records inside the specified timeframe.

    """
    response_details = UrgencyQueryResponseDetails(distance=0.05, urgency_rule="rule")

    response = UrgencyQueryResponseExtract(
        details={str(i): response_details for i in range(100)},
        is_urgent=True,
        matched_rules=["rule"],
        response_datetime_utc="2020-01-01T01:00:00",
        urgency_response_id=1,
    )

    urgency_query = UrgencyQuery(
        message_datetime_utc="2020-01-01T01:00:00",
        message_text="Urgent text!",
        response=response,
        urgency_query_id=1,
        workspace_id=0,
    )

    fake_aaqv2.add_urgency_queries(urgency_query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    urgency_queries = aaqv2.urgency_queries.get_urgency_queries(
        start_date=start_date, end_date=end_date
    )

    assert_frame_equal(urgency_queries, LazyFrame([urgency_query.to_dict()]))


def test_get_urgency_queries_single_record_outside_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the urgency queries endpoint, and no records exist
    within the requested timeframe, an empty DataFrame is returned.

    """
    urgency_query = UrgencyQuery(
        urgency_query_id=1,
        message_text="Urgent text!",
        message_datetime_utc="2020-01-01T00:00:00",
        response=None,
        workspace_id=0,
    )

    fake_aaqv2.add_urgency_queries(urgency_query)

    start_date = "2020-01-01T01:00:00"
    end_date = "2020-01-02T00:00:00"
    urgency_queries = aaqv2.urgency_queries.get_urgency_queries(
        start_date=start_date, end_date=end_date
    )

    assert urgency_queries.collect().is_empty()


@pytest.mark.xfail(
    reason="Not implemented yet: should raise an error instead of dropping extra fields"
)
def test_urgency_queries_with_extra_struct_field(fake_aaqv2, aaqv2):
    """
    Tests that an extra struct in the urgency queries response details causes an error.
    This is expected to fail as Polars silently drops unexpected struct fields.
    We would prefer these unexpected fields to cause pipeline failures.
    """
    response_details = UrgencyQueryResponseDetails(distance=0.05, urgency_rule="rule")

    # Adds an extra response detail struct to the details field.
    # This should fail as the existing schema has 100 fields.
    response = UrgencyQueryResponseExtract(
        details={str(i): response_details for i in range(101)},
        is_urgent=True,
        matched_rules=["rule"],
        response_datetime_utc="2020-01-01T01:00:00",
        urgency_response_id=1,
    )

    urgency_query = UrgencyQuery(
        message_datetime_utc="2020-01-01T01:00:00",
        message_text="Urgent text!",
        response=response,
        urgency_query_id=1,
        workspace_id=0,
    )

    fake_aaqv2.add_urgency_queries(urgency_query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"

    with pytest.raises(SchemaError):
        aaqv2.urgency_queries.get_urgency_queries(
            start_date=start_date, end_date=end_date
        )


@pytest.mark.xfail(
    reason="Not implemented yet: should raise an error instead of dropping extra fields"
)
def test_queries_fails_with_extra_struct_field(fake_aaqv2, aaqv2):
    """
    Tests that an extra field in search_results will cause an error.
    This is expected to fail as Polars silently drops unexpected struct fields.
    We would prefer these unexpected fields to cause pipeline failures.
    """
    search_results = SearchResults(title="Title", text="text", id=0, distance=0.05)

    query_response = QueryResponse(
        response_id=1,
        search_results={
            "0": search_results,
            "1": search_results,
            "2": search_results,
            "3": {
                "title": "Title",
                "text": "text",
                "id": 0,
                "distance": 0.05,
                "unexpected_field": True,  # type: ignore
            },
        },
        llm_response="response",
        response_datetime_utc="2020-01-01T00:00:00",
    )

    response_feedback = ResponseFeedback(
        feedback_id=1,
        feedback_sentiment="Bad",
        feedback_text=None,
        feedback_datetime_utc="2020-01-01T00:00:00",
    )

    content_feedback = ContentFeedback(
        feedback_id=1,
        feedback_sentiment="Bad",
        feedback_text="Bad",
        feedback_datetime_utc="2020-01-01T00:00:00",
        content_id=1,
    )

    query = Query(
        query_id=1,
        query_text="This is my query.",
        query_metadata="Some metadata",
        query_datetime_utc="2020-01-01T00:00:00",
        response=[query_response],
        response_feedback=[response_feedback],
        content_feedback=[content_feedback],
        workspace_id=0,
    )

    fake_aaqv2.add_queries(query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"

    with pytest.raises(SchemaError):
        aaqv2.queries.get_queries(start_date=start_date, end_date=end_date)


@typing.no_type_check
def test_get_contents_schema_null_integrity(fake_aaqv2, aaqv2):
    """
    Test that the contents schema is maintained when fields have no value

    """
    content = Content(
        content_title=None,
        content_text=None,
        content_tags=None,
        content_metadata=None,
        is_archived=None,
        content_id=None,
        display_number=None,
        created_datetime_utc=None,
        negative_votes=None,
        positive_votes=None,
        updated_datetime_utc=None,
        workspace_id=None,
    )

    fake_aaqv2.add_contents(content)

    contents = aaqv2.contents.get_contents()

    assert contents.collect_schema() == contents_schema


@typing.no_type_check
def test_get_urgency_rules_schema_null_integrity(fake_aaqv2, aaqv2):
    """
    Test that the urgency rules schema is maintained when fields have no value

    """
    urgency_rule = UrgencyRule(
        urgency_rule_metadata=None,
        urgency_rule_text=None,
        created_datetime_utc=None,
        updated_datetime_utc=None,
        urgency_rule_id=None,
        workspace_id=None,
    )

    fake_aaqv2.add_urgency_rules(urgency_rule)

    urgency_rules = aaqv2.urgency_rules.get_urgency_rules()

    assert urgency_rules.collect_schema() == urgency_rules_schema


@typing.no_type_check
def test_get_urgency_queries_schema_null_integrity(fake_aaqv2, aaqv2):
    """
    Test that the urgency queries schema is maintained when fields have no value

    """
    urgency_query = UrgencyQuery(
        message_datetime_utc="2020-01-01T00:00:00",
        message_text=None,
        response=None,
        urgency_query_id=None,
        workspace_id=None,
    )
    fake_aaqv2.add_urgency_queries(urgency_query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    urgency_queries = aaqv2.urgency_queries.get_urgency_queries(
        start_date=start_date, end_date=end_date
    )

    assert urgency_queries.collect_schema() == urgency_queries_schema


@typing.no_type_check
def test_get_queries_schema_null_integrity(fake_aaqv2, aaqv2):
    """
    Test that the queries schema is maintained when fields have no value

    """
    query = Query(
        query_id=None,
        query_text=None,
        query_metadata=None,
        query_datetime_utc="2020-01-01T00:00:00",
        response=None,
        response_feedback=None,
        content_feedback=None,
        workspace_id=None,
    )

    fake_aaqv2.add_queries(query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    queries = aaqv2.queries.get_queries(start_date=start_date, end_date=end_date)

    assert queries.collect_schema() == queries_schema


def test_get_contents_schema_empty_response(aaqv2):
    """
    Test that the contents schema is maintained when the response is empty

    """

    contents = aaqv2.contents.get_contents()

    assert contents.collect_schema() == contents_schema


def test_get_urgency_rules_schema_empty_response(aaqv2):
    """
    Test that the urgency rules schema is maintained when fields have no value

    """
    urgency_rules = aaqv2.urgency_rules.get_urgency_rules()

    assert urgency_rules.collect_schema() == urgency_rules_schema


def test_get_urgency_queries_schema_empty_response(aaqv2):
    """
    Test that the urgency queries schema is maintained when fields have no value

    """

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    urgency_queries = aaqv2.urgency_queries.get_urgency_queries(
        start_date=start_date, end_date=end_date
    )

    assert urgency_queries.collect_schema() == urgency_queries_schema


def test_get_queries_schema_empty_response(aaqv2):
    """
    Test that the queries schema is maintained when fields have no value

    """

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    queries = aaqv2.queries.get_queries(start_date=start_date, end_date=end_date)

    assert queries.collect_schema() == queries_schema
