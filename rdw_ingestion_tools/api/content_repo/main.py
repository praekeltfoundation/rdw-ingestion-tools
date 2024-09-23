from api.content_repo.requests.page_views import PageViews
from api.content_repo.requests.pages import Pages

from . import client


class pyContent:
    """A wrapper class for the various Content Repo endpoints."""

    pageviews = PageViews(client)
    pages = Pages(client)
