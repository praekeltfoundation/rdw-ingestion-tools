from attrs import define, field
from httpx import Client

from api.content_repo.requests.page_views import PageViews
from api.content_repo.requests.pages import Pages

from . import client as default_client


@define
class pyContent:
    """A wrapper class for the various Content Repo endpoints.

    The client is configurable to it can be switched out in tests.

    """

    client: Client = field(factory=lambda: default_client)

    pageviews: PageViews = field(init=False)
    pages: Pages = field(init=False)

    def __attrs_post_init__(self):
        self.pageviews = PageViews(client=self.client)
        self.pages = Pages(client=self.client)
