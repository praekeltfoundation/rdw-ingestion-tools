from api.aaqv2 import pyAAQV2

urgency_queries = pyAAQV2.urgency_queries.get_urgency_queries()

urgency_queries.head(5)
