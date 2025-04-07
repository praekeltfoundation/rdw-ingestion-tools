import pytest
from api.aaqv2 import pyAAQV2
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from .fake_aaqv2.api import FakeAAQV2
from .fake_aaqv2.models import (
    Content,
    ContentFeedback,
    Query,
    QueryResponse,
    ResponseFeedback,
    UrgencyQuery,
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
        content_metadata={"type": "profound"},
        is_archived=False,
        content_id=1,
        user_id=1,
        created_datetime_utc="2020-01-01T00:00:00",
        updated_datetime_utc="2020-01-01T00:00:01",
        positive_votes=0,
        negative_votes=100,
    )

    fake_aaqv2.add_contents(content)

    contents = aaqv2.contents.get_contents()

    assert_frame_equal(contents, DataFrame([content.to_dict()]))


def test_get_urgency_rules_single_record(fake_aaqv2, aaqv2):
    """
    When get is called against the urgency rules endpoint a correct dataframe of
    urgency rules is returned.

    """
    urgency_rule = UrgencyRule(
        created_datetime_utc="2020-01-01T00:00:00",
        updated_datetime_utc="2020-01-01T00:00:00",
        urgency_rule_id=1,
        urgency_rule_metadata={"type": "urgent"},
        urgency_rule_text="S.O.S.",
        user_id=156,
    )

    fake_aaqv2.add_urgency_rules(urgency_rule)

    urgency_rules = aaqv2.urgency_rules.get_urgency_rules()

    assert_frame_equal(urgency_rules, DataFrame([urgency_rule.to_dict()]))


def test_get_queries_single_record_in_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the queries endpoint a correct dataframe of
    queries is returned with records inside the specified timeframe.

    """
    query_response = QueryResponse(
        response_id=1,
        search_results=[],
        llm_response=None,
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
        feedback_text=None,
        feedback_datetime_utc="2020-01-01T00:00:00",
        content_id=1,
    )

    query = Query(
        query_id=1,
        user_id=1,
        query_text="This is my query.",
        query_metadata="Some metadata",
        query_datetime_utc="2020-01-01T01:00:00",
        response=[query_response],
        response_feedback=[response_feedback],
        content_feedback=[content_feedback],
    )

    fake_aaqv2.add_queries(query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    queries = aaqv2.queries.get_queries(start_date=start_date, end_date=end_date)

    assert_frame_equal(queries, DataFrame([query.to_dict()]))


def test_get_queries_single_record_outside_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the queries endpoint, and no records exist within
    the requested timeframe, an empty DataFrame is returned.

    """
    query_response = QueryResponse(
        response_id=1,
        search_results=[],
        llm_response=None,
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
        feedback_text=None,
        feedback_datetime_utc="2020-01-01T00:00:00",
        content_id=1,
    )

    query = Query(
        query_id=1,
        user_id=1,
        query_text="This is my query.",
        query_metadata="Some metadata",
        query_datetime_utc="2020-01-01T00:00:00",
        response=[query_response],
        response_feedback=[response_feedback],
        content_feedback=[content_feedback],
    )

    fake_aaqv2.add_queries(query)

    start_date = "2020-01-01T01:00:00"
    end_date = "2020-01-02T00:00:00"
    queries = aaqv2.queries.get_queries(start_date=start_date, end_date=end_date)

    assert_frame_equal(queries, DataFrame())


def test_get_urgency_queries_single_record_in_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the urgency queries endpoint a correct dataframe of
    urgency queries is returned with records inside the specified timeframe.

    """
    urgency_query = UrgencyQuery(
        urgency_query_id=1,
        user_id=1,
        message_text="Urgent text!",
        message_datetime_utc="2020-01-01T01:00:00",
        response=None,
    )

    fake_aaqv2.add_urgency_queries(urgency_query)

    start_date = "2020-01-01T00:00:00"
    end_date = "2020-01-02T00:00:00"
    urgency_queries = aaqv2.urgency_queries.get_urgency_queries(
        start_date=start_date, end_date=end_date
    )

    assert_frame_equal(urgency_queries, DataFrame([urgency_query.to_dict()]))


def test_get_urgency_queries_single_record_outside_timeframe(fake_aaqv2, aaqv2):
    """
    When get is called against the urgency queries endpoint, and no records exist
    within the requested timeframe, an empty DataFrame is returned.

    """
    urgency_query = UrgencyQuery(
        urgency_query_id=1,
        user_id=1,
        message_text="Urgent text!",
        message_datetime_utc="2020-01-01T00:00:00",
        response=None,
    )

    fake_aaqv2.add_urgency_queries(urgency_query)

    start_date = "2020-01-01T01:00:00"
    end_date = "2020-01-02T00:00:00"
    urgency_queries = aaqv2.urgency_queries.get_urgency_queries(
        start_date=start_date, end_date=end_date
    )

    assert_frame_equal(urgency_queries, DataFrame())
