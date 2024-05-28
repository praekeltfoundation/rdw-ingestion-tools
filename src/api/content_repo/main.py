from api.content_repo.requests.page_views import PageViews
from api.content_repo.requests.pages import Pages

from . import client


class pyContent:
    pageviews = PageViews(client)
    pages = Pages(client)
