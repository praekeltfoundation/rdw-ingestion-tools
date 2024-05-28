from datetime import datetime

from api.content_repo import pyContent

start_time = datetime.strptime("2024-01-01", "%Y-%m-%d").isoformat()

pageviews = pyContent.pageviews.get_pageviews(ts=start_time)

pageviews.head(5)
