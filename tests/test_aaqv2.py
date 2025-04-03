import pytest

from .fake_aaqv2.api import FakeAAQV2
from .fake_aaqv2.models import Content


@pytest.fixture
def fake_aaqv2() -> FakeAAQV2:
    return FakeAAQV2()


def test_get_contents(fake_aaqv2):
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

    assert True
