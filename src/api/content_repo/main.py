from api.content_repo.requests.page_views import PageViews
from api.content_repo.requests.pages import Pages

from . import session


class pyContent:
    pageviews = PageViews(session)
    pages = Pages(session)
