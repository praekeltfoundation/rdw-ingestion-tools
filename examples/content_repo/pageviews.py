from datetime import datetime

from api.content_repo import pyContent

start_time = datetime(2024, 1, 1).isoformat()

pageviews = pyContent().pageviews.get_pageviews(ts=start_time)

pageviews.head(5)
