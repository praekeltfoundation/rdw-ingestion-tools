from api.content_repo.requests.page_views import PageViews

from . import session


class pyContent:

    pageviews = PageViews(session)
