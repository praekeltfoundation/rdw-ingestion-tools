import pytest
from api.aaqv2 import pyAAQV2
from pandas import DataFrame
from pandas.testing import assert_frame_equal

from .fake_aaqv2.api import FakeAAQV2
from .fake_aaqv2.models import Content, UrgencyRule


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
